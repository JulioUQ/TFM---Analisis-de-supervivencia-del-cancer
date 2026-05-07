# ═══════════════════════════════════════════════════════════════════════════════
#  FUNCIONES — Kaplan-Meier
# ═══════════════════════════════════════════════════════════════════════════════

import matplotlib.ticker as mticker

import os
import re
import math
import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, to_rgb

import textwrap

from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test


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

def plot_km_global(
    kmf: KaplanMeierFitter,
    n_total: int,
    output_path: str = ".",
    group_name: str = "Global",
    dataset_name: str = "Dataset",
    title: str = None,
    subtitle: str = None,
    ci_show: bool = True,
    ci_alpha: float = 0.15,
    time_points: tuple = (60, 120, 240),
    risk_table_points: tuple = None
) -> None:
    """
    Curva Kaplan-Meier global con banda de confianza, línea de mediana,
    supervivencias en puntos clave y tabla at-risk.

    Parámetros
    ----------
    kmf : KaplanMeierFitter
        Objeto KaplanMeierFitter ya ajustado.

    n_total : int
        Número total de pacientes/observaciones.

    output_path : str
        Carpeta donde guardar el HTML o ruta completa terminada en .html.

    group_name : str
        Nombre del análisis o grupo. Se muestra en el título.

    dataset_name : str
        Nombre del dataset o cohorte. Se muestra en el subtítulo y nombre del archivo.

    title : str, optional
        Título personalizado. Si no se indica, se genera automáticamente.

    subtitle : str, optional
        Subtítulo personalizado. Si no se indica, se genera automáticamente.

    ci_show : bool
        Si True, muestra intervalo de confianza.

    ci_alpha : float
        Transparencia del intervalo de confianza.

    time_points : tuple
        Puntos temporales donde anotar supervivencia, por defecto 5, 10 y 20 años.

    risk_table_points : tuple, optional
        Puntos temporales para la tabla at-risk. Si no se indica, se generan automáticamente.

    Retorna
    -------
    None
    """

    survival = kmf.survival_function_
    x = survival.index
    y = survival.iloc[:, 0]

    max_time = float(np.nanmax(x)) if len(x) > 0 else 0

    if risk_table_points is None:
        if max_time > 0:
            risk_table_points = tuple(
                np.linspace(0, max_time, 6).round(0).astype(int)
            )
        else:
            risk_table_points = (0,)

    fig = make_subplots(
        rows=2,
        cols=1,
        row_heights=[0.78, 0.22],
        vertical_spacing=0.10,
        specs=[
            [{"type": "scatter"}],
            [{"type": "table"}]
        ]
    )

    main_color = "steelblue"
    median_color = "firebrick"

    if ci_show:
        ci_x, ci_lower, ci_upper = _km_confidence_interval(kmf)

        fig.add_trace(
            go.Scatter(
                x=ci_x,
                y=ci_lower,
                mode="lines",
                line=dict(width=0, shape="hv"),
                showlegend=False,
                hoverinfo="skip"
            ),
            row=1,
            col=1
        )

        fig.add_trace(
            go.Scatter(
                x=ci_x,
                y=ci_upper,
                mode="lines",
                line=dict(width=0, shape="hv"),
                fill="tonexty",
                fillcolor=_plotly_rgba(main_color, alpha=ci_alpha),
                name="IC 95%",
                showlegend=True,
                hoverinfo="skip"
            ),
            row=1,
            col=1
        )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line=dict(color=main_color, width=2.4, shape="hv"),
            name="Supervivencia global",
            hovertemplate=(
                "Tiempo = %{x:.2f} meses<br>"
                "S(t) = %{y:.1%}"
                "<extra></extra>"
            )
        ),
        row=1,
        col=1
    )

    mediana = kmf.median_survival_time_

    if mediana is not None and np.isfinite(mediana):
        fig.add_vline(
            x=mediana,
            line=dict(color=median_color, width=1.4, dash="dash"),
            opacity=0.85,
            row=1,
            col=1
        )

        fig.add_hline(
            y=0.5,
            line=dict(color=median_color, width=1.4, dash="dash"),
            opacity=0.85,
            row=1,
            col=1
        )

        fig.add_annotation(
            x=mediana,
            y=0.52,
            text=f"Mediana: {mediana:.1f} m<br>({mediana / 12:.1f} años)",
            showarrow=True,
            arrowhead=2,
            ax=45,
            ay=-35,
            font=dict(size=11, color=median_color),
            bgcolor="rgba(255,255,255,0.80)",
            bordercolor=median_color,
            borderwidth=1,
            row=1,
            col=1
        )

    point_colors = px.colors.qualitative.Safe + px.colors.qualitative.Pastel

    for i, t in enumerate(time_points):
        if t <= max_time:
            st = float(kmf.predict(t))
            color = point_colors[i % len(point_colors)]

            fig.add_trace(
                go.Scatter(
                    x=[t],
                    y=[st],
                    mode="markers+text",
                    marker=dict(size=9, color=color),
                    text=[f"S({int(t // 12)}a)={st:.2f}"],
                    textposition="top right",
                    textfont=dict(size=11, color=color),
                    name=f"S({int(t // 12)} años)",
                    hovertemplate=(
                        f"Tiempo = {t:.0f} meses<br>"
                        f"S(t) = {st:.1%}"
                        "<extra></extra>"
                    )
                ),
                row=1,
                col=1
            )

    at_risk_values = []

    event_table = kmf.event_table

    for t in risk_table_points:
        valid_times = event_table.index[event_table.index <= t]

        if len(valid_times) == 0:
            at_risk = n_total
        else:
            at_risk = int(event_table.loc[valid_times[-1], "at_risk"])

        at_risk_values.append(at_risk)

    fig.add_trace(
        go.Table(
            header=dict(
                values=["<b>Tiempo (meses)</b>"] + [str(t) for t in risk_table_points],
                fill_color="white",
                align="center",
                font=dict(size=12, color="#1f2c56"),
                line_color="lightgray"
            ),
            cells=dict(
                values=[
                    ["<b>N en riesgo</b>"],
                    *[[f"{v:,}"] for v in at_risk_values]
                ],
                fill_color="white",
                align="center",
                font=dict(size=12),
                line_color="lightgray",
                height=28
            )
        ),
        row=2,
        col=1
    )

    main_title = title or f"{group_name}"
    sub_title = subtitle or f"Cohorte: {dataset_name} · n = {n_total:,}"

    fig.update_xaxes(
        title_text="Tiempo (meses)",
        gridcolor="lightgray",
        zerolinecolor="lightgray",
        automargin=True,
        row=1,
        col=1
    )

    fig.update_yaxes(
        title_text="Probabilidad de supervivencia S(t)",
        range=[0, 1.05],
        tickformat=".0%",
        gridcolor="lightgray",
        zerolinecolor="lightgray",
        automargin=True,
        row=1,
        col=1
    )

    fig.update_layout(
        height=650,
        width=1200,
        title=dict(
            text=(
                f"<span style='font-size: 24px;'><b>{main_title}</b></span>"
                f"<br><span style='color: gray;'>{sub_title}</span>"
            ),
            x=0.5,
            y=0.96,
            xanchor="center",
            yanchor="top"
        ),
        margin=dict(t=145, b=80, l=80, r=80),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
            bgcolor="rgba(255,255,255,0.75)",
            bordercolor="lightgray",
            borderwidth=1
        )
    )

    if output_path:
        if str(output_path).lower().endswith(".html"):
            file_path = output_path
            output_dir = os.path.dirname(file_path)

            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
        else:
            os.makedirs(output_path, exist_ok=True)

            safe_group = _safe_filename(group_name)
            safe_dataset = _safe_filename(dataset_name)

            file_path = os.path.join(
                output_path,
                f"{safe_dataset}_km_global_{safe_group}.html"
            )

        fig.write_html(file_path)
        print(f"✔ KM global guardado en: {file_path}")

    fig.show()


def _wrap_legend_label(label: str, width: int = 22) -> str:
    """
    Envuelve etiquetas largas de la leyenda en varias líneas.
    """
    label = str(label)

    if len(label) <= width:
        return label

    return "<br>".join(
        textwrap.wrap(label, width=width, break_long_words=False)
    )

def _safe_filename(value: str) -> str:
    value = str(value)
    value = value.replace(" ", "_").replace("/", "_")
    value = re.sub(r"[^A-Za-z0-9_\-\.]", "", value)
    return value


def _plotly_rgba(color, alpha=0.08):
    color = str(color)

    if color.startswith("rgb"):
        nums = re.findall(r"[\d\.]+", color)
        r, g, b = nums[:3]
        return f"rgba({int(float(r))},{int(float(g))},{int(float(b))},{alpha})"

    r, g, b = to_rgb(color)
    return f"rgba({int(r * 255)},{int(g * 255)},{int(b * 255)},{alpha})"


def _build_palette(n, cmap=None):
    if n <= 0:
        return []

    if cmap is not None:
        try:
            mpl_cmap = plt.get_cmap(cmap)
            return [
                to_hex(mpl_cmap(x))
                for x in np.linspace(0.1, 0.85, n)
            ]
        except Exception:
            pass

    base_palette = px.colors.qualitative.Safe + px.colors.qualitative.Pastel
    return [base_palette[i % len(base_palette)] for i in range(n)]


def _km_confidence_interval(kmf):
    ci = kmf.confidence_interval_survival_function_

    lower_cols = [c for c in ci.columns if "lower" in c.lower()]
    upper_cols = [c for c in ci.columns if "upper" in c.lower()]

    if lower_cols and upper_cols:
        lower = ci[lower_cols[0]]
        upper = ci[upper_cols[0]]
    else:
        lower = ci.iloc[:, 0]
        upper = ci.iloc[:, 1]

    return ci.index, lower, upper


def plot_km_groups(
    df: pd.DataFrame,
    grupos_config: dict,
    group_name: str = "Subgrupos clínicos",
    dataset_name: str = "Dataset",
    title: str = None,
    subtitle: str = None,
    ncols: int = 2,
    nrow: int = None,
    output_path: str = ".",
    duration_col: str = "duration",
    event_col: str = "event",
    ci_show: bool = True,
    ci_alpha: float = 0.08
) -> None:
    """
    Grid de curvas Kaplan-Meier estratificadas por múltiples variables.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con columnas de duración, evento y variables de agrupación.

    grupos_config : dict
        Diccionario con formato:
        {
            "Título subplot": ("columna_grupo", "cmap")
        }

    group_name : str
        Nombre del grupo de variables analizado. Se usa en el título principal.

    dataset_name : str
        Nombre del dataset o cohorte. Se usa en el subtítulo y nombre del archivo.

    title : str, optional
        Título personalizado. Si no se indica, se genera automáticamente.

    subtitle : str, optional
        Subtítulo personalizado. Si no se indica, se genera automáticamente.

    ncols : int
        Número de columnas del grid.

    nrow : int, optional
        Número máximo de filas a mostrar. Si se indica, limita el número de plots.

    output_path : str
        Carpeta donde guardar el HTML o ruta completa terminada en .html.

    duration_col : str
        Nombre de la columna de duración.

    event_col : str
        Nombre de la columna de evento. Debe ser 1 = evento, 0 = censura.

    ci_show : bool
        Si True, muestra intervalos de confianza.

    ci_alpha : float
        Transparencia del intervalo de confianza.

    Retorna
    -------
    None
    """

    required_cols = {duration_col, event_col}
    missing_base = required_cols - set(df.columns)

    if missing_base:
        raise ValueError(f"Faltan columnas obligatorias en df: {missing_base}")

    if not grupos_config:
        print(f"No hay variables configuradas para '{group_name}'.")
        return

    items = list(grupos_config.items())

    if nrow is not None:
        max_vars = nrow * ncols
        if len(items) > max_vars:
            print(
                f"⚠ Se muestran las primeras {max_vars} variables "
                f"({nrow} filas × {ncols} cols)."
            )
        items = items[:max_vars]

    n_plots = len(items)

    if n_plots == 0:
        print(f"No hay curvas KM para '{group_name}'.")
        return

    nrows = nrow if nrow is not None else math.ceil(n_plots / ncols)

    plot_specs = []

    for subplot_title, config in items:
        if len(config) == 2:
            col, cmap = config
        else:
            raise ValueError(
                "Cada entrada de grupos_config debe tener formato "
                "{'Título': ('columna', 'cmap')}"
            )

        if col not in df.columns:
            plot_specs.append({
                "titulo": subplot_title,
                "col": col,
                "fitters": {},
                "grupos": [],
                "palette": [],
                "stats": f"Columna no encontrada: {col}"
            })
            continue

        data = df[[duration_col, event_col, col]].dropna().copy()
        data = data[data[duration_col] >= 0]

        grupos = sorted(data[col].unique(), key=lambda x: str(x))
        fitters = {}

        for grupo in grupos:
            subset = data[data[col] == grupo]

            if subset.empty:
                continue

            kmf = KaplanMeierFitter(label=str(grupo))
            kmf.fit(
                durations=subset[duration_col],
                event_observed=subset[event_col],
                label=str(grupo)
            )
            fitters[grupo] = kmf

        if len(grupos) >= 2 and len(data) > 0:
            lr = multivariate_logrank_test(
                event_durations=data[duration_col],
                groups=data[col],
                event_observed=data[event_col]
            )

            p = lr.p_value
            sig = (
                "***" if p < 0.001 else
                "**" if p < 0.01 else
                "*" if p < 0.05 else
                "ns"
            )

            stats = (
                f"Log-rank χ²={lr.test_statistic:.2f} · "
                f"p={p:.2e} · {sig}"
            )
        else:
            stats = "Log-rank no aplicable: menos de 2 grupos"

        palette = _build_palette(len(grupos), cmap=cmap)

        plot_specs.append({
            "titulo": subplot_title,
            "col": col,
            "fitters": fitters,
            "grupos": grupos,
            "palette": palette,
            "stats": stats
        })

    if nrows > 1:
        max_allowed_spacing = 1.0 / (nrows - 1)
        safe_vertical_spacing = min(0.22, max_allowed_spacing * 0.75)
    else:
        safe_vertical_spacing = 0.05

    subplot_titles = [
        (
            f"<b>{spec['titulo']}</b>"
            f"<br><span style='font-size:11px; color:gray;'>{spec['stats']}</span>"
        )
        for spec in plot_specs
    ]

    fig = make_subplots(
        rows=nrows,
        cols=ncols,
        subplot_titles=subplot_titles,
        horizontal_spacing=0.08,
        vertical_spacing=safe_vertical_spacing
    )

    legend_specs = []

    for i, spec in enumerate(plot_specs):
        row_pos = (i // ncols) + 1
        col_pos = (i % ncols) + 1

        subplot_idx = i + 1
        legend_name = "legend" if subplot_idx == 1 else f"legend{subplot_idx}"

        col = spec["col"]
        fitters = spec["fitters"]
        palette = spec["palette"]

        if not fitters:
            xref = "x domain" if subplot_idx == 1 else f"x{subplot_idx} domain"
            yref = "y domain" if subplot_idx == 1 else f"y{subplot_idx} domain"

            fig.add_annotation(
                text="Sin datos suficientes",
                x=0.5,
                y=0.5,
                xref=xref,
                yref=yref,
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            continue

        max_label_len = max(len(str(g)) for g in spec["grupos"]) if spec["grupos"] else 0

        legend_specs.append({
            "subplot_idx": subplot_idx,
            "legend_name": legend_name,
            "n_groups": len(spec["grupos"]),
            "max_label_len": max_label_len
        })

        for j, (grupo, kmf) in enumerate(fitters.items()):
            color = palette[j % len(palette)]
            legend_group = f"{col}_{grupo}_{subplot_idx}"

            survival = kmf.survival_function_
            x = survival.index
            y = survival.iloc[:, 0]

            if ci_show:
                ci_x, ci_lower, ci_upper = _km_confidence_interval(kmf)

                fig.add_trace(
                    go.Scatter(
                        x=ci_x,
                        y=ci_lower,
                        mode="lines",
                        line=dict(width=0, shape="hv"),
                        showlegend=False,
                        hoverinfo="skip",
                        legendgroup=legend_group
                    ),
                    row=row_pos,
                    col=col_pos
                )

                fig.add_trace(
                    go.Scatter(
                        x=ci_x,
                        y=ci_upper,
                        mode="lines",
                        line=dict(width=0, shape="hv"),
                        fill="tonexty",
                        fillcolor=_plotly_rgba(color, alpha=ci_alpha),
                        showlegend=False,
                        hoverinfo="skip",
                        legendgroup=legend_group
                    ),
                    row=row_pos,
                    col=col_pos
                )

            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="lines",
                    line=dict(color=color, width=2.1, shape="hv"),
                    name=_wrap_legend_label(str(grupo), width=24),
                    legend=legend_name,
                    legendgroup=legend_group,
                    showlegend=True,
                    hovertemplate=(
                        f"<b>{spec['titulo']}</b><br>"
                        f"{col} = {grupo}<br>"
                        "Tiempo = %{x:.2f} meses<br>"
                        "S(t) = %{y:.1%}"
                        "<extra></extra>"
                    )
                ),
                row=row_pos,
                col=col_pos
            )

        fig.update_xaxes(
            title_text="Tiempo (meses)",
            gridcolor="lightgray",
            zerolinecolor="lightgray",
            automargin=True,
            row=row_pos,
            col=col_pos
        )

        fig.update_yaxes(
            title_text="S(t)",
            range=[0, 1.05],
            tickformat=".0%",
            gridcolor="lightgray",
            zerolinecolor="lightgray",
            automargin=True,
            row=row_pos,
            col=col_pos
        )

    main_title = title or f"Curvas de Kaplan-Meier: {group_name}"
    sub_title = subtitle or f"Cohorte: {dataset_name}"

    altura_figura = max(550, 420 * nrows)

    fig.update_layout(
        height=altura_figura,
        width=1250,
        title=dict(
            text=(
                f"<span style='font-size: 24px;'><b>{main_title}</b></span>"
                f"<br><span style='color: gray;'>{sub_title}</span>"
            ),
            x=0.5,
            y=0.96,
            xanchor="center",
            yanchor="top"
        ),
        margin=dict(t=165, b=90, l=80, r=80),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12),
        showlegend=True
    )

    fig.update_annotations(font_size=12)

    # ------------------------------------------------------------
    # Leyenda independiente por subplot, evitando solapamiento:
    # - si hay muchas categorías o labels largos, se reserva espacio
    #   a la derecha del subplot reduciendo el dominio del eje X.
    # ------------------------------------------------------------
    for spec in legend_specs:
        subplot_idx = spec["subplot_idx"]
        legend_key = spec["legend_name"]
        n_groups = spec["n_groups"]
        max_label_len = spec["max_label_len"]

        axis_suffix = "" if subplot_idx == 1 else str(subplot_idx)
        xaxis_key = f"xaxis{axis_suffix}"
        yaxis_key = f"yaxis{axis_suffix}"

        x_domain = list(fig.layout[xaxis_key].domain)
        y_domain = list(fig.layout[yaxis_key].domain)

        cell_width = x_domain[1] - x_domain[0]

        # Espacio reservado dinámicamente para la leyenda
        if n_groups >= 10 or max_label_len >= 28:
            reserved_space = 0.14
            font_size = 8
        elif n_groups >= 7 or max_label_len >= 20:
            reserved_space = 0.11
            font_size = 8
        elif n_groups >= 5 or max_label_len >= 14:
            reserved_space = 0.08
            font_size = 9
        else:
            reserved_space = 0.00
            font_size = 9

        # Evitar dejar el gráfico demasiado estrecho
        min_plot_width = 0.16
        reserved_space = min(reserved_space, max(0.0, cell_width - min_plot_width))

        if reserved_space > 0:
            new_x_domain = [x_domain[0], x_domain[1] - reserved_space]
            fig.layout[xaxis_key].domain = new_x_domain

            legend_x = new_x_domain[1] + 0.005
            legend_xanchor = "left"
            legend_bg = "rgba(255,255,255,0.88)"
        else:
            new_x_domain = x_domain
            legend_x = new_x_domain[1] - 0.01
            legend_xanchor = "right"
            legend_bg = "rgba(255,255,255,0.78)"

        fig.update_layout(**{
            legend_key: dict(
                x=legend_x,
                y=y_domain[1] - 0.01,
                xanchor=legend_xanchor,
                yanchor="top",
                bgcolor=legend_bg,
                bordercolor="lightgray",
                borderwidth=1,
                font=dict(size=font_size),
                orientation="v",
                traceorder="normal",
                itemsizing="trace"
            )
        })

    if output_path:
        if str(output_path).lower().endswith(".html"):
            file_path = output_path
            output_dir = os.path.dirname(file_path)

            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
        else:
            os.makedirs(output_path, exist_ok=True)

            safe_group = _safe_filename(group_name)
            safe_dataset = _safe_filename(dataset_name)

            file_path = os.path.join(
                output_path,
                f"{safe_dataset}_km_subplots_{safe_group}.html"
            )

        fig.write_html(file_path)
        print(f"✔ KM subplots guardado en: {file_path}")

    fig.show()

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