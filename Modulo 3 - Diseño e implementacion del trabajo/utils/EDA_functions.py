# ---------------------------------------------------------
# LIBRERIAS NECESARIAS   
# ---------------------------------------------------------
import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

import pandas as pd

import numpy as np
import math

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# ---------------------------------------------------------
# FUNCIONES REUTILIZABLES PARA EDA
# ---------------------------------------------------------
# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

def describe_df(data):
    """
    Proporciona un resumen del DataFrame, incluyendo tipos de datos, estadísticas básicas,
    conteo de valores nulos, valores únicos, mediana, rango de fechas y top categorías.

    :param data: DataFrame de pandas.
    :return: DataFrame con el resumen del DataFrame dado.
    """

    # ---- Print del tamaño del DataFrame ----
    print(f"Dimensiones del DataFrame: {data.shape[0]} filas, {data.shape[1]} columnas\n")

    total = len(data)

    # ---- Resumen base ----
    summary = pd.DataFrame({
        'Column': data.columns,
        'Data Type': data.dtypes.astype(str),
        'Non-null Count': data.count().values,
        '% Null Values': ((data.isnull().sum() / total) * 100).round(2).values,
        'Unique Values': data.nunique().values
    })

    # ---- Columna TopCounts (categóricas y fechas) ----
    def get_top_counts(col):
        counts = col.value_counts(dropna=True).head(3)
        return ", ".join([f"{idx} ({cnt})" for idx, cnt in counts.items()])

    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    datetime_cols = data.select_dtypes(include=['datetime', 'datetime64[ns]']).columns

    summary['TopCounts'] = None

    for col in categorical_cols.union(datetime_cols):
        summary.loc[summary['Column'] == col, 'TopCounts'] = get_top_counts(data[col])

    # ---- Estadísticas para columnas numéricas ----
    numeric_cols = data.select_dtypes(include=['number']).columns
    if not numeric_cols.empty:
        describe_stats = (
            data[numeric_cols]
            .describe()
            .T
            .rename(columns={'50%': 'median'})[
                ['mean', 'median', 'std', 'min', '25%', '75%', 'max']
            ]
            .reset_index()
            .rename(columns={'index': 'Column'})
        )

        summary = pd.merge(summary, describe_stats, on='Column', how='left')

    # ---- Rango de fechas para columnas datetime ----
    if not datetime_cols.empty:
        date_ranges = pd.DataFrame({
            'Column': datetime_cols,
            'Min Date': data[datetime_cols].min().values,
            'Max Date': data[datetime_cols].max().values
        })

        summary = pd.merge(summary, date_ranges, on='Column', how='left')

    return summary

# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

def null_summary(data): 
    """
    Devuelve un resumen de las columnas del DataFrame que contienen valores nulos.
    Incluye: Column, Non-null Count, Null Count, % Null Values y TotalCount.

    :param data: DataFrame de pandas.
    :return: DataFrame con el resumen de las columnas del DataFrame que contienen valores nulos.
    """
    # Crear base del resumen
    total = len(data)
    summary = pd.DataFrame({
        'Column': data.columns,
        'Data Type': data.dtypes.astype(str),
        'Non-null Count': data.count().values,
        'Null Count': data.isnull().sum().values,
        '% Null Values': ((data.isnull().sum() / total) * 100).round(2).values,
        'TotalCount': total
    })
    
    # Filtrar y ordenar solo columnas con valores nulos
    summary = summary[summary['Null Count'] > 0]
    summary = summary.sort_values(by='% Null Values', ascending=False).reset_index(drop=True)

    
    return summary

# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

def unique_df(df):
    """
    Imprime un resumen de las categorías únicas para las variables categóricas de un DataFrame.

    :param df: DataFrame de pandas.
    """
    categorical_columns = df.select_dtypes(include=['category', 'object']).columns

    if len(categorical_columns) == 0:
        print("No se encontraron columnas categóricas u objeto en el DataFrame.")
        return

    for column in categorical_columns:
        print(f"Resumen para la columna '{column}':\n{df[column].unique()}\n")
        
# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

def plot_categorical_subplots(df, group_name, dataset_name="Dataset", columns=None, output_path="."):
    """
    Genera subplots para variables categóricas detectadas automáticamente
    o especificadas manualmente.
    """

    if columns is None:
        valid_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    else:
        valid_cols = [col for col in columns if col in df.columns]

    n_cols = len(valid_cols)

    if n_cols == 0:
        print(f"No hay variables categóricas para '{group_name}'.")
        return

    max_cols_per_row = 3
    n_rows = math.ceil(n_cols / max_cols_per_row)
    subplot_titles = [f"<b>{col}</b>" for col in valid_cols]

    if n_rows > 1:
        max_allowed_spacing = 1.0 / (n_rows - 1)
        safe_vertical_spacing = min(0.18, max_allowed_spacing * 0.75)
    else:
        safe_vertical_spacing = 0.05

    fig = make_subplots(
        rows=n_rows, cols=max_cols_per_row,
        subplot_titles=subplot_titles,
        horizontal_spacing=0.08,
        vertical_spacing=safe_vertical_spacing
    )

    color_palette = px.colors.qualitative.Plotly + px.colors.qualitative.Set1

    for i, col in enumerate(valid_cols):
        row_pos = (i // max_cols_per_row) + 1
        col_pos = (i % max_cols_per_row) + 1

        df_clean = df.dropna(subset=[col])
        conteo = df_clean[col].value_counts().reset_index()
        conteo.columns = ['Categoría', 'Frecuencia']

        fig.add_trace(
            go.Bar(
                x=conteo['Categoría'].astype(str),
                y=conteo['Frecuencia'],
                name=col[:15],
                marker=dict(
                    color=color_palette[:len(conteo)],
                    line=dict(color='white', width=1)
                ),
                text=conteo['Frecuencia'],
                textposition='outside'
            ),
            row=row_pos, col=col_pos
        )

        fig.update_xaxes(tickangle=-45, row=row_pos, col=col_pos, tickfont=dict(size=10))

        if col_pos == 1:
            fig.update_yaxes(title_text="Frecuencia", row=row_pos, col=col_pos)

    altura_figura = max(500, 350 * n_rows)

    fig.update_layout(
        height=altura_figura,
        width=1200,
        showlegend=False,
        title=dict(
            text=f"<span style='font-size: 24px;'><b>Análisis de Variables: {group_name}</b></span><br><span style='color: gray;'>Cohorte: {dataset_name}</span>",
            x=0.5, y=0.98, xanchor="center", yanchor="top"
        ),
        margin=dict(t=160, b=80, l=70, r=70),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12)
    )

    fig.update_yaxes(gridcolor='lightgray', zerolinecolor='lightgray')

    # ── Guardar en el directorio recibido como parámetro ──────────────────────
    os.makedirs(output_path, exist_ok=True)
    safe_name = group_name.replace(' ', '_').replace('/', '_')
    file_path = os.path.join(output_path, f"{dataset_name}_cat_{safe_name}.html")
    fig.write_html(file_path)

    print(f"✔ Categorical subplots guardado en: {file_path}")
    fig.show()


# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

def plot_numerical_subplots(df, group_name, dataset_name="Dataset", columns=None, output_path="."):
    """
    Genera histogramas para variables numéricas detectadas automáticamente
    o especificadas manualmente.
    """

    if columns is None:
        valid_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    else:
        valid_cols = [
            col for col in columns
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col])
        ]

    n_cols = len(valid_cols)

    if n_cols == 0:
        print(f"No hay variables numéricas para '{group_name}'.")
        return

    max_cols_per_row = 3
    n_rows = math.ceil(n_cols / max_cols_per_row)
    subplot_titles = [f"<b>{col}</b>" for col in valid_cols]

    if n_rows > 1:
        max_allowed_spacing = 1.0 / (n_rows - 1)
        safe_vertical_spacing = min(0.18, max_allowed_spacing * 0.75)
    else:
        safe_vertical_spacing = 0.05

    fig = make_subplots(
        rows=n_rows, cols=max_cols_per_row,
        subplot_titles=subplot_titles,
        horizontal_spacing=0.08,
        vertical_spacing=safe_vertical_spacing
    )

    color_palette = px.colors.qualitative.Safe + px.colors.qualitative.Pastel

    for i, col in enumerate(valid_cols):
        row_pos = (i // max_cols_per_row) + 1
        col_pos = (i % max_cols_per_row) + 1

        serie_limpia = df[col].dropna()

        fig.add_trace(
            go.Histogram(
                x=serie_limpia,
                name=col[:15],
                marker_color=color_palette[i % len(color_palette)],
                marker_line=dict(color='white', width=1),
                opacity=0.85,
                nbinsx=40
            ),
            row=row_pos, col=col_pos
        )

        if col_pos == 1:
            fig.update_yaxes(title_text="Frecuencia", row=row_pos, col=col_pos)

    altura_figura = max(500, 350 * n_rows)

    fig.update_layout(
        height=altura_figura,
        width=1200,
        showlegend=False,
        title=dict(
            text=f"<span style='font-size: 24px;'><b>Análisis de Variables Numéricas: {group_name}</b></span><br><span style='color: gray;'>Cohorte: {dataset_name}</span>",
            x=0.5, y=0.98, xanchor="center", yanchor="top"
        ),
        margin=dict(t=160, b=80, l=70, r=70),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12),
        bargap=0.05
    )

    fig.update_yaxes(gridcolor='lightgray', zerolinecolor='lightgray')

    # ── Guardar en el directorio recibido como parámetro ──────────────────────
    os.makedirs(output_path, exist_ok=True)
    safe_name = group_name.replace(' ', '_').replace('/', '_')
    file_path = os.path.join(output_path, f"{dataset_name}_num_subplots_{safe_name}.html")
    fig.write_html(file_path)

    print(f"✔ Numerical subplots guardado en: {file_path}")
    fig.show()


# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

def plot_correlation_heatmap(
    df,
    dataset_name="Dataset",
    method="pearson",
    figsize=(18, 14),
    output_path=".",       
    top_n=5                
):
    """
    Genera y guarda un heatmap de correlación, lo muestra en pantalla
    e imprime un cuadro resumen con las top_n correlaciones más altas y más bajas.
    """

    df_num = df.select_dtypes(include=[np.number])

    if df_num.shape[1] < 2:
        print("No hay suficientes variables numéricas.")
        return

    corr = df_num.corr(method=method)

    # ── Heatmap ───────────────────────────────────────────────────────────────
    mask = np.triu(np.ones_like(corr, dtype=bool))

    plt.figure(figsize=figsize)

    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"shrink": 0.8, "label": "Coeficiente de Correlación"},
        square=True,
    )

    plt.title(
        f"Mapa de Calor de Correlaciones\n{dataset_name}",
        fontsize=16,
        pad=20,
    )

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    # ── Guardar en el directorio recibido como parámetro ──────────────────────
    os.makedirs(output_path, exist_ok=True)
    file_path = os.path.join(output_path, f"{dataset_name}_heatmap_correlaciones.png")
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    print(f"✔ Heatmap guardado en: {file_path}")
    plt.show()

    # ── Resumen de correlaciones extremas ─────────────────────────────────────
    corr_pairs = (
        corr.where(np.tril(np.ones(corr.shape), k=-1).astype(bool))
            .stack()
            .dropna()                          # ← elimina pares con NaN
            .reset_index()
    )
    corr_pairs.columns = ["Variable A", "Variable B", "Correlación"]
    corr_pairs["Correlación"] = corr_pairs["Correlación"].round(4)
    corr_pairs_sorted = corr_pairs.sort_values("Correlación", ascending=False).reset_index(drop=True)

    top_high = corr_pairs_sorted.head(top_n)
    top_low  = corr_pairs_sorted.tail(top_n).sort_values("Correlación").reset_index(drop=True)

    # Anchura dinámica según el par más largo
    max_len = max(
        (len(f"{r['Variable A']}  ↔  {r['Variable B']}") 
         for _, r in pd.concat([top_high, top_low]).iterrows()),
        default=40
    )
    col_w = max(max_len, 40)
    total_w = col_w + 18

    print(f"\n{'═' * total_w}")
    print(f"  Resumen de Correlaciones — {dataset_name} ({method.capitalize()})")
    print(f"{'═' * total_w}")
    print(f"  {'Etiqueta':<10} {'Par de variables':<{col_w}} {'Corr':>7}")
    print(f"  {'─'*10} {'─'*col_w} {'─'*7}")

    for i, (_, row) in enumerate(top_high.iterrows()):
        par = f"{row['Variable A']}  ↔  {row['Variable B']}"
        print(f"  {'▲ Top ' + str(i+1):<10} {par:<{col_w}} {row['Correlación']:>7.4f}")

    print(f"  {'·'*10} {'·'*col_w} {'·'*7}")   # separador visual entre altas y bajas

    for i, (_, row) in enumerate(top_low.iterrows()):
        par = f"{row['Variable A']}  ↔  {row['Variable B']}"
        print(f"  {'▼ Bot ' + str(i+1):<10} {par:<{col_w}} {row['Correlación']:>7.4f}")

    print(f"{'═' * total_w}\n")