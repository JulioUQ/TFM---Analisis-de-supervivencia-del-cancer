# ═══════════════════════════════════════════════════════════════════════════════
#  FUNCIONES — Kaplan-Meier
# ═══════════════════════════════════════════════════════════════════════════════

from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd


# ── 1. Ajuste del estimador ────────────────────────────────────────────────────

def fit_km_global(durations: np.ndarray,
                  events: np.ndarray,
                  label: str = 'Cohorte completa') -> KaplanMeierFitter:
    """
    Ajusta un estimador KM sobre la cohorte completa.

    Parámetros
    ----------
    durations : array de tiempos (meses)
    events    : array binario (1 = evento, 0 = censurado)
    label     : etiqueta para la curva

    Retorna
    -------
    KaplanMeierFitter ajustado
    """
    kmf = KaplanMeierFitter()
    kmf.fit(durations, event_observed=events, label=label)
    return kmf


def fit_km_by_group(df: pd.DataFrame,
                    col: str,
                    duration_col: str = 'duration',
                    event_col: str    = 'event') -> dict:
    """
    Ajusta un KaplanMeierFitter por cada categoría de `col`.

    Retorna
    -------
    dict {categoria: KaplanMeierFitter}
    """
    fitters = {}
    grupos  = sorted(df[col].dropna().unique())
    for grupo in grupos:
        mask = df[col] == grupo
        kmf  = KaplanMeierFitter()
        kmf.fit(
            df.loc[mask, duration_col],
            event_observed = df.loc[mask, event_col],
            label          = f'{grupo} (n={mask.sum()})'
        )
        fitters[grupo] = kmf
    return fitters


# ── 2. Métricas ────────────────────────────────────────────────────────────────

def km_metrics(kmf: KaplanMeierFitter,
               horizons: list = [60, 120, 180, 240]) -> pd.DataFrame:
    """
    Extrae métricas clave de un KaplanMeierFitter:
      · Mediana de supervivencia (IC 95%)
      · S(t) en horizontes temporales definidos

    Parámetros
    ----------
    kmf      : KaplanMeierFitter ajustado
    horizons : lista de tiempos en meses para evaluar S(t)

    Retorna
    -------
    DataFrame con las métricas
    """
    mediana    = kmf.median_survival_time_
    ci_low     = kmf.confidence_interval_cumulative_density_\
                    .iloc[:, 0]  # lower bound survival
    ci_high    = kmf.confidence_interval_cumulative_density_\
                    .iloc[:, 1]

    rows = [{'Métrica': 'Mediana supervivencia (meses)',
              'Valor' : f"{mediana:.1f}"}]
    for t in horizons:
        st = kmf.predict(t)
        rows.append({'Métrica': f'S(t={t}m)  [{t//12} años]',
                     'Valor'  : f"{st:.3f}"})
    return pd.DataFrame(rows)


def logrank_summary(df: pd.DataFrame,
                    variables: list,
                    duration_col: str = 'duration',
                    event_col: str    = 'event') -> pd.DataFrame:
    """
    Aplica el test log-rank multivariante a cada variable de `variables`
    y devuelve una tabla resumen ordenada por p-valor.

    Retorna
    -------
    DataFrame con columnas: Variable, k_grupos, chi2, p-valor, Significancia
    """
    rows = []
    for col in variables:
        if col not in df.columns:
            continue
        lr = multivariate_logrank_test(df[duration_col], df[col], df[event_col])
        p  = lr.p_value
        k  = df[col].nunique()
        rows.append({
            'Variable'     : col,
            'k grupos'     : k,
            'chi²'         : round(lr.test_statistic, 3),
            'p-valor'      : round(p, 6),
            'Significancia': '***' if p < 0.001 else
                             ('**'  if p < 0.01  else
                             ('*'   if p < 0.05  else 'ns'))
        })
    return pd.DataFrame(rows).sort_values('p-valor').reset_index(drop=True)


# ── 3. Visualizaciones ────────────────────────────────────────────────────────

def plot_km_global(kmf: KaplanMeierFitter,
                   n_total: int,
                   output_path: str = None) -> None: # type: ignore
    """
    Curva KM global con banda de confianza, línea de mediana y
    tabla at-risk (número de pacientes en riesgo por intervalos).
    """
    fig, ax = plt.subplots(figsize=(11, 5))

    kmf.plot_survival_function(
        ax=ax, ci_show=True, ci_alpha=0.15,
        color='steelblue', linewidth=2
    )

    mediana = kmf.median_survival_time_
    ax.axvline(mediana, color='firebrick', linestyle='--', linewidth=1.3, alpha=0.85)
    ax.axhline(0.5,     color='firebrick', linestyle='--', linewidth=1.3, alpha=0.85)
    ax.text(mediana + 4, 0.52,
            f'Mediana: {mediana:.1f} m\n({mediana/12:.1f} años)',
            color='firebrick', fontsize=10)

    # Supervivencias clave
    for t, color in [(60, '#2ca02c'), (120, '#ff7f0e'), (240, '#9467bd')]:
        st = kmf.predict(t)
        ax.scatter(t, st, zorder=5, color=color, s=40)
        ax.text(t + 2, st + 0.02, f'S({t//12}a)={st:.2f}', # type: ignore
                fontsize=8.5, color=color)

    ax.set_xlabel('Tiempo (meses)', fontsize=12)
    ax.set_ylabel('Probabilidad de supervivencia  S(t)', fontsize=12)
    ax.set_title(f'Curva de Kaplan-Meier — METABRIC  (n = {n_total:,})',
                 fontsize=13, fontweight='bold')
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    ax.grid(alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.show()


def plot_km_groups(df: pd.DataFrame,
                   grupos_config: dict,
                   ncols: int       = 2,
                   output_path: str = None) -> None: # type: ignore
    """
    Grid de curvas KM estratificadas por múltiples variables.

    Parámetros
    ----------
    df            : DataFrame con duration, event y las variables de agrupación
    grupos_config : dict  {titulo: (columna, cmap)}
    ncols         : columnas del grid
    output_path   : ruta de guardado
    """
    n_plots = len(grupos_config)
    nrows   = int(np.ceil(n_plots / ncols))

    fig, axes = plt.subplots(nrows, ncols,
                              figsize=(8 * ncols, 5.5 * nrows))
    axes = np.array(axes).flatten()

    for idx, (titulo, (col, cmap)) in enumerate(grupos_config.items()):
        ax = axes[idx]

        fitters = fit_km_by_group(df, col)
        grupos  = sorted(df[col].dropna().unique())
        palette = plt.get_cmap(cmap)(np.linspace(0.1, 0.85, len(grupos)))

        for i, (grupo, kmf) in enumerate(fitters.items()):
            kmf.plot_survival_function(
                ax=ax, ci_show=True, ci_alpha=0.08,
                color=palette[i], linewidth=1.8
            )

        # Log-rank
        lr  = multivariate_logrank_test(df['duration'], df[col], df['event'])
        p   = lr.p_value
        sig = '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else 'ns'))

        ax.set_title(f'{titulo}\nLog-rank  χ²={lr.test_statistic:.2f}  '
                     f'p={p:.2e}  {sig}',
                     fontsize=10.5, fontweight='bold')
        ax.set_xlabel('Tiempo (meses)', fontsize=10)
        ax.set_ylabel('S(t)', fontsize=10)
        ax.set_ylim(0, 1.05)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7.5, loc='upper right',
                  framealpha=0.7, ncol=1 if len(grupos) <= 4 else 2)

    # Ocultar ejes sobrantes
    for j in range(idx + 1, len(axes)):
        axes[j].set_visible(False)

    plt.suptitle('Curvas de Kaplan-Meier por subgrupos clínicos — METABRIC',
                 fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.show()


def plot_logrank_heatmap(tabla_lr: pd.DataFrame,
                         output_path: str = None) -> None: # type: ignore
    """
    Heatmap visual del p-valor log-rank para todas las variables analizadas.
    Facilita la comparación rápida de la significancia pronóstica.
    """
    tabla_plot = tabla_lr.copy()
    tabla_plot['-log10(p)'] = -np.log10(tabla_plot['p-valor'].clip(lower=1e-16))

    fig, ax = plt.subplots(figsize=(5, len(tabla_plot) * 0.45 + 1.5))

    colors = ['#d73027' if p < 0.001 else
              '#f46d43' if p < 0.01  else
              '#fdae61' if p < 0.05  else
              '#abd9e9'
              for p in tabla_plot['p-valor']]

    bars = ax.barh(tabla_plot['Variable'][::-1],
                   tabla_plot['-log10(p)'][::-1],
                   color=colors[::-1], alpha=0.85, height=0.65)

    ax.axvline(-np.log10(0.05),  color='#fdae61', linestyle='--',
               linewidth=1.2, label='p = 0.05')
    ax.axvline(-np.log10(0.01),  color='#f46d43', linestyle='--',
               linewidth=1.2, label='p = 0.01')
    ax.axvline(-np.log10(0.001), color='#d73027', linestyle='--',
               linewidth=1.2, label='p = 0.001')

    ax.set_xlabel('−log₁₀(p-valor log-rank)', fontsize=11)
    ax.set_title('Significancia pronóstica por variable\n(test log-rank)',
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='lower right')
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.show()