# ── 0. Imports y configuración ───────────────────────────────────────────────
import os
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from IPython.display import display, Markdown

from sklearn.model_selection import StratifiedKFold
from statsmodels.stats.outliers_influence import variance_inflation_factor

from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import proportional_hazard_test, multivariate_logrank_test

from sksurv.util import Surv
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sksurv.metrics import (
    concordance_index_censored,
    brier_score,
    integrated_brier_score,
)

warnings.filterwarnings('ignore')

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

FIG_DIR = Path('../images/Modelos/Cox')
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ── 4. Funciones auxiliares Cox-LASSO ────────────────────────────────────────
def get_coef_vector(model: CoxnetSurvivalAnalysis, feature_names, alpha: float) -> pd.Series:
    """Extrae coeficientes para el alpha más cercano disponible en el modelo."""
    alphas = np.asarray(model.alphas_)
    idx = int(np.argmin(np.abs(alphas - alpha)))
    coefs = model.coef_[:, idx]
    return pd.Series(coefs, index=feature_names, name='coef')


def coefficients_table(model, feature_names, alpha, tol=1e-8):
    coef = get_coef_vector(model, feature_names, alpha)
    tab = (
        coef[coef.abs() > tol]
        .rename('coef')
        .reset_index()
        .rename(columns={'index': 'Variable'})
    )
    tab['HR'] = np.exp(tab['coef'])
    tab['abs_coef'] = tab['coef'].abs()
    tab['Dirección'] = np.where(tab['coef'] > 0, '↑ riesgo', '↓ riesgo')
    return tab.sort_values('abs_coef', ascending=False).reset_index(drop=True)


def select_cox_lasso_alpha_cv(X, y, n_alphas=80, n_splits=5, random_state=42):
    """Selecciona alpha por CV maximizando C-index."""
    # Ruta inicial de alphas ajustada en train completo. No toca test.
    path_model = CoxnetSurvivalAnalysis(
        l1_ratio=1.0,
        n_alphas=n_alphas,
        alpha_min_ratio=0.01, # type: ignore
        max_iter=100000,
        fit_baseline_model=False,
    )
    path_model.fit(X, y)
    alpha_grid = np.asarray(path_model.alphas_)
    
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    rows = []
    
    strat = y['event'].astype(int)
    for fold, (tr_idx, va_idx) in enumerate(cv.split(X, strat), start=1):
        X_tr, X_va = X.iloc[tr_idx], X.iloc[va_idx]
        y_tr, y_va = y[tr_idx], y[va_idx]
        
        model = CoxnetSurvivalAnalysis(
            l1_ratio=1.0,
            alphas=alpha_grid,
            max_iter=100000,
            fit_baseline_model=False,
        )
        model.fit(X_tr, y_tr)
        
        for alpha in model.alphas_:
            try:
                risk = model.predict(X_va, alpha=alpha)
                cidx = concordance_index_censored(y_va['event'], y_va['time'], risk)[0]
            except Exception:
                cidx = np.nan
            rows.append({'fold': fold, 'alpha': alpha, 'c_index': cidx})
    
    cv_raw = pd.DataFrame(rows).dropna()
    summary = (
        cv_raw
        .groupby('alpha', as_index=False)
        .agg(c_index_cv_mean=('c_index', 'mean'), c_index_cv_std=('c_index', 'std'))
        .sort_values('c_index_cv_mean', ascending=False)
        .reset_index(drop=True)
    )
    best_alpha = float(summary.loc[0, 'alpha']) # type: ignore
    return best_alpha, summary, cv_raw, alpha_grid

# ── 3. Diagnóstico VIF ───────────────────────────────────────────────────────
def compute_vif_table(X: pd.DataFrame) -> pd.DataFrame:
    """Calcula VIF para una matriz numérica. Devuelve inf si hay colinealidad perfecta."""
    X_num = X.select_dtypes(include='number').copy()
    # Elimina columnas constantes si existieran.
    nunique = X_num.nunique(dropna=False)
    constant_cols = nunique[nunique <= 1].index.tolist()
    X_num = X_num.drop(columns=constant_cols, errors='ignore')
    
    rows = []
    values = X_num.values
    for i, col in enumerate(X_num.columns):
        try:
            vif = variance_inflation_factor(values, i)
        except Exception:
            vif = np.inf
        rows.append({'Variable': col, 'VIF': vif})
    
    out = pd.DataFrame(rows).sort_values('VIF', ascending=False).reset_index(drop=True)
    return out


def plot_alpha_cv(summary, best_alpha, save_path=None):
    fig, ax = plt.subplots(figsize=(9, 5))
    x = summary['alpha'].values
    y = summary['c_index_cv_mean'].values
    yerr = summary['c_index_cv_std'].fillna(0).values
    
    order = np.argsort(x)
    ax.errorbar(x[order], y[order], yerr=yerr[order], marker='o', linewidth=1.5, capsize=3)
    ax.axvline(best_alpha, linestyle='--', linewidth=1.5, label=f'alpha óptimo = {best_alpha:.3g}')
    ax.set_xscale('log')
    ax.set_xlabel('alpha / lambda — escala log')
    ax.set_ylabel('C-index medio en validación')
    ax.set_title('Selección de penalización Cox-LASSO mediante validación cruzada')
    ax.grid(alpha=0.3)
    ax.legend()
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=160, bbox_inches='tight')
    plt.show()


# ── 7. Visualización de coeficientes seleccionados ───────────────────────────
def plot_cox_coefficients(coef_table, top_n=25, save_path=None):
    plot_df = coef_table.head(top_n).copy().sort_values('coef')
    fig, ax = plt.subplots(figsize=(9, max(6, 0.32 * len(plot_df))))
    ax.barh(plot_df['Variable'], plot_df['coef'])
    ax.axvline(0, color='black', linewidth=1)
    ax.set_xlabel('Coeficiente Cox-LASSO')
    ax.set_title(f'Top {len(plot_df)} coeficientes por magnitud absoluta')
    ax.grid(axis='x', alpha=0.25)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=160, bbox_inches='tight')
    plt.show()