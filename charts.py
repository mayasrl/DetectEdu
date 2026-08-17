import pandas as pd
import plotly.graph_objects as go

from models import CLASSIFICACAO_CORES, CLASSIFICACAO_LABELS

PALETA = {
    "borda": "#2A2D3E",
    "texto_primario": "#E8EAF0",
    "texto_secundario": "#AEB5C8",
    "destaque": "#5B8DEF",
    "roxo": "#9C6FE4",
}

LAYOUT_BASE = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": "Arial, sans-serif",
        "color": PALETA["texto_primario"],
        "size": 14,
    },
    "margin": {"l": 30, "r": 20, "t": 55, "b": 35},
}


def grafico_distribuicao_classificacao(metricas: dict) -> go.Figure:
    categorias = [
        CLASSIFICACAO_LABELS["sem_indicios"],
        CLASSIFICACAO_LABELS["atencao"],
        CLASSIFICACAO_LABELS["intervencao"],
    ]
    valores = [
        metricas.get("sem_indicios", 0),
        metricas.get("atencao", 0),
        metricas.get("intervencao", 0),
    ]
    cores = [
        CLASSIFICACAO_CORES["sem_indicios"],
        CLASSIFICACAO_CORES["atencao"],
        CLASSIFICACAO_CORES["intervencao"],
    ]

    figura = go.Figure(
        go.Pie(
            labels=categorias,
            values=valores,
            hole=0.62,
            marker={"colors": cores, "line": {"color": "#0F1117", "width": 2}},
            textinfo="value+percent",
            textfont={"size": 14},
            hovertemplate="%{label}<br>%{value} aluno(s) · %{percent}<extra></extra>",
        )
    )
    figura.update_layout(
        **LAYOUT_BASE,
        title={"text": "Distribuição por classificação", "font": {"size": 18}},
        showlegend=True,
        legend={
            "orientation": "h",
            "yanchor": "top",
            "y": -0.08,
            "xanchor": "center",
            "x": 0.5,
            "font": {"size": 12},
        },
        annotations=[
            {
                "text": f"<b>{sum(valores)}</b><br><span style='font-size:12px'>alunos</span>",
                "x": 0.5,
                "y": 0.5,
                "font": {"size": 19, "color": PALETA["texto_primario"]},
                "showarrow": False,
            }
        ],
    )
    return figura


def grafico_dispersao_frequencia_nota(dataframe: pd.DataFrame) -> go.Figure:
    dados = dataframe.dropna(subset=["Frequência (%)", "Nota Provas"])
    if dados.empty:
        return go.Figure()

    mapa_cores = {
        CLASSIFICACAO_LABELS["sem_indicios"]: CLASSIFICACAO_CORES["sem_indicios"],
        CLASSIFICACAO_LABELS["atencao"]: CLASSIFICACAO_CORES["atencao"],
        CLASSIFICACAO_LABELS["intervencao"]: CLASSIFICACAO_CORES["intervencao"],
    }

    figura = go.Figure()

    for classificacao, cor in mapa_cores.items():
        grupo = dados[dados["Classificação"] == classificacao]
        if grupo.empty:
            continue

        figura.add_trace(
            go.Scatter(
                x=grupo["Frequência (%)"],
                y=grupo["Nota Provas"],
                mode="markers",
                name=classificacao,
                text=grupo["Aluno"],
                marker={
                    "size": 12,
                    "color": cor,
                    "line": {"width": 1, "color": PALETA["borda"]},
                },
                hovertemplate=(
                    "<b>%{text}</b><br>Frequência: %{x:.1f}%<br>Nota: %{y:.1f}<extra></extra>"
                ),
            )
        )

    figura.add_vline(
        x=75,
        line_dash="dot",
        line_color=CLASSIFICACAO_CORES["intervencao"],
        opacity=0.55,
    )
    figura.add_hline(
        y=6,
        line_dash="dot",
        line_color=CLASSIFICACAO_CORES["intervencao"],
        opacity=0.55,
    )
    figura.update_layout(
        **LAYOUT_BASE,
        title={"text": "Frequência x desempenho", "font": {"size": 18}},
        xaxis_title="Frequência (%)",
        yaxis_title="Nota de provas (0–10)",
        yaxis={
            "range": [0, 10.5],
            "gridcolor": PALETA["borda"],
            "zerolinecolor": PALETA["borda"],
            "tickfont": {"size": 12},
        },
        xaxis={
            "range": [0, 105],
            "gridcolor": PALETA["borda"],
            "zerolinecolor": PALETA["borda"],
            "tickfont": {"size": 12},
        },
        legend={
            "bgcolor": "rgba(0,0,0,0)",
            "font": {"size": 12},
        },
    )
    return figura


def grafico_medias_turma(dataframe: pd.DataFrame) -> go.Figure:
    if dataframe.empty:
        return go.Figure()

    medias = [
        ("Frequência", dataframe["Frequência (%)"].mean() / 10),
        ("Provas", dataframe["Nota Provas"].mean()),
        ("Atividades", dataframe["Nota Atividades"].mean()),
        ("Participação", dataframe["Participação"].mean()),
    ]

    media_exercicios = dataframe["Taxa Exercícios (%)"].mean()
    if pd.notna(media_exercicios):
        medias.append(("Exercícios", media_exercicios / 10))

    medias = [(categoria, valor) for categoria, valor in medias if pd.notna(valor)]
    if not medias:
        return go.Figure()

    categorias = [categoria for categoria, _ in medias]
    valores = [valor for _, valor in medias]

    figura = go.Figure(
        go.Bar(
            x=valores,
            y=categorias,
            orientation="h",
            marker_color=PALETA["destaque"],
            text=[f"{valor:.1f}" for valor in valores],
            textposition="outside",
            cliponaxis=False,
        )
    )
    figura.update_layout(
        **LAYOUT_BASE,
        title={"text": "Média dos principais indicadores", "font": {"size": 18}},
        xaxis={
            "range": [0, 10.8],
            "gridcolor": PALETA["borda"],
            "zerolinecolor": PALETA["borda"],
            "title": "Escala comparável (0–10)",
        },
        yaxis={"autorange": "reversed", "tickfont": {"size": 13}},
        showlegend=False,
    )
    return figura


def grafico_evolucao_aluno(dataframe: pd.DataFrame) -> go.Figure:
    if dataframe.empty:
        return go.Figure()

    figura = go.Figure()
    figura.add_trace(
        go.Scatter(
            x=dataframe["Data"],
            y=dataframe["Nota Provas"],
            mode="lines+markers",
            name="Nota de provas",
            line={"color": PALETA["destaque"], "width": 3},
            marker={"size": 8},
        )
    )
    figura.add_trace(
        go.Scatter(
            x=dataframe["Data"],
            y=dataframe["Nota Atividades"],
            mode="lines+markers",
            name="Nota de atividades",
            line={"color": PALETA["roxo"], "width": 3, "dash": "dash"},
            marker={"size": 8},
        )
    )
    figura.update_layout(
        **LAYOUT_BASE,
        title={"text": "Evolução do desempenho", "font": {"size": 18}},
        yaxis_title="Nota padronizada",
        xaxis_title="Data do registro",
        yaxis={
            "range": [0, 10.5],
            "gridcolor": PALETA["borda"],
            "zerolinecolor": PALETA["borda"],
        },
        xaxis={
            "gridcolor": PALETA["borda"],
            "zerolinecolor": PALETA["borda"],
        },
        legend={"bgcolor": "rgba(0,0,0,0)", "font": {"size": 12}},
    )
    return figura


def grafico_radar_aluno(indicadores: dict) -> go.Figure:
    categorias = [
        "Frequência",
        "Nota de provas",
        "Nota de atividades",
        "Participação",
    ]
    valores = [
        min(indicadores["frequencia"] / 10, 10),
        indicadores["nota_provas"],
        indicadores["nota_atividades"],
        indicadores["participacao"],
    ]

    if indicadores["taxa_exercicios"] is not None:
        categorias.append("Taxa de exercícios")
        valores.append(min(indicadores["taxa_exercicios"] / 10, 10))

    figura = go.Figure(
        go.Scatterpolar(
            r=valores + [valores[0]],
            theta=categorias + [categorias[0]],
            fill="toself",
            fillcolor="rgba(91, 141, 239, 0.18)",
            line={"color": PALETA["destaque"], "width": 3},
            marker={"size": 7},
        )
    )
    figura.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        polar={
            "bgcolor": "rgba(0,0,0,0)",
            "radialaxis": {
                "visible": True,
                "range": [0, 10],
                "gridcolor": PALETA["borda"],
                "color": PALETA["texto_secundario"],
                "tickfont": {"size": 11},
            },
            "angularaxis": {
                "gridcolor": PALETA["borda"],
                "color": PALETA["texto_primario"],
                "tickfont": {"size": 12},
            },
        },
        font={
            "family": "Arial, sans-serif",
            "color": PALETA["texto_primario"],
            "size": 14,
        },
        margin={"l": 55, "r": 55, "t": 55, "b": 45},
        title={"text": "Perfil dos indicadores", "font": {"size": 18}},
        showlegend=False,
    )
    return figura


def grafico_comparativo_turma(dataframe: pd.DataFrame) -> go.Figure:
    dados = dataframe.dropna(subset=["Nota Provas"]).copy()
    if dados.empty:
        return go.Figure()

    dados = dados.sort_values("Nota Provas")
    cores = (
        dados["classificacao_key"]
        .map(CLASSIFICACAO_CORES)
        .fillna(PALETA["texto_secundario"])
    )

    figura = go.Figure(
        go.Bar(
            x=dados["Nota Provas"],
            y=dados["Aluno"],
            orientation="h",
            marker_color=cores.tolist(),
            text=dados["Nota Provas"].round(1),
            textposition="outside",
            cliponaxis=False,
        )
    )
    figura.update_layout(
        **LAYOUT_BASE,
        height=max(480, len(dados) * 24),
        title={"text": "Nota de provas por aluno", "font": {"size": 18}},
        xaxis_title="Nota (0–10)",
        xaxis={
            "range": [0, 10.8],
            "gridcolor": PALETA["borda"],
            "zerolinecolor": PALETA["borda"],
        },
        yaxis={
            "gridcolor": "rgba(0,0,0,0)",
            "tickfont": {"size": 12},
        },
        showlegend=False,
    )
    return figura
