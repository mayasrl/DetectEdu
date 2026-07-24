import pandas as pd
import plotly.graph_objects as go

from models import (
    CLASSIFICACAO_CORES,
    CLASSIFICACAO_LABELS,
)

PALETA = {
    "borda": "#2A2D3E",
    "texto_primario": "#E8EAF0",
    "texto_secundario": "#9BA3BB",
    "destaque": "#5B8DEF",
}

LAYOUT_BASE = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": "Arial, sans-serif",
        "color": PALETA["texto_primario"],
        "size": 13,
    },
    "margin": {
        "l": 20,
        "r": 20,
        "t": 40,
        "b": 20,
    },
    "xaxis": {
        "gridcolor": PALETA["borda"],
        "zerolinecolor": PALETA["borda"],
    },
    "yaxis": {
        "gridcolor": PALETA["borda"],
        "zerolinecolor": PALETA["borda"],
    },
}


def grafico_distribuicao_classificacao(
    metricas: dict,
) -> go.Figure:
    categorias = [
        "Sem indícios",
        "Atenção pedagógica",
        "Necessita intervenção",
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
        go.Bar(
            x=categorias,
            y=valores,
            marker_color=cores,
            text=valores,
            textposition="outside",
            textfont={
                "size": 15,
                "color": PALETA["texto_primario"],
            },
        )
    )
    figura.update_layout(
        **LAYOUT_BASE,
        title={
            "text": "Distribuição por classificação",
            "font": {"size": 15},
        },
        yaxis_title="Número de alunos",
        showlegend=False,
    )
    return figura


def grafico_dispersao_frequencia_nota(
    dataframe: pd.DataFrame,
) -> go.Figure:
    dados = dataframe.dropna(
        subset=["Frequência (%)", "Nota Provas"]
    )
    if dados.empty:
        return go.Figure()

    mapa_cores = {
        CLASSIFICACAO_LABELS[
            "sem_indicios"
        ]: CLASSIFICACAO_CORES["sem_indicios"],
        CLASSIFICACAO_LABELS[
            "atencao"
        ]: CLASSIFICACAO_CORES["atencao"],
        CLASSIFICACAO_LABELS[
            "intervencao"
        ]: CLASSIFICACAO_CORES["intervencao"],
    }

    figura = go.Figure()

    for classificacao, cor in mapa_cores.items():
        grupo = dados[
            dados["Classificação"] == classificacao
        ]
        if grupo.empty:
            continue

        figura.add_trace(
            go.Scatter(
                x=grupo["Frequência (%)"],
                y=grupo["Nota Provas"],
                mode="markers+text",
                name=classificacao,
                text=grupo["Aluno"],
                textposition="top center",
                textfont={"size": 10},
                marker={
                    "size": 10,
                    "color": cor,
                    "line": {
                        "width": 1,
                        "color": PALETA["borda"],
                    },
                },
            )
        )

    figura.add_vline(
        x=75,
        line_dash="dot",
        line_color=CLASSIFICACAO_CORES[
            "intervencao"
        ],
        opacity=0.5,
    )
    figura.add_hline(
        y=6,
        line_dash="dot",
        line_color=CLASSIFICACAO_CORES[
            "intervencao"
        ],
        opacity=0.5,
    )
    figura.update_layout(
        **LAYOUT_BASE,
        title={
            "text": "Relação entre frequência e desempenho",
            "font": {"size": 15},
        },
        xaxis_title="Frequência (%)",
        yaxis_title="Nota de provas (0–10)",
        yaxis={
            "range": [0, 10.5],
            "gridcolor": PALETA["borda"],
        },
        xaxis={
            "range": [0, 105],
            "gridcolor": PALETA["borda"],
        },
        legend={
            "bgcolor": "rgba(0,0,0,0)",
            "bordercolor": PALETA["borda"],
        },
    )
    return figura


def grafico_evolucao_aluno(
    dataframe: pd.DataFrame,
) -> go.Figure:
    if dataframe.empty:
        return go.Figure()

    figura = go.Figure()
    figura.add_trace(
        go.Scatter(
            x=dataframe["Data"],
            y=dataframe["Nota Provas"],
            mode="lines+markers",
            name="Nota de provas",
            line={
                "color": PALETA["destaque"],
                "width": 2,
            },
            marker={"size": 7},
        )
    )
    figura.add_trace(
        go.Scatter(
            x=dataframe["Data"],
            y=dataframe["Nota Atividades"],
            mode="lines+markers",
            name="Nota de atividades",
            line={
                "color": "#9C6FE4",
                "width": 2,
                "dash": "dash",
            },
            marker={"size": 7},
        )
    )
    figura.update_layout(
        **LAYOUT_BASE,
        title={
            "text": "Evolução do desempenho",
            "font": {"size": 15},
        },
        yaxis_title="Nota padronizada",
        xaxis_title="Data do registro",
        yaxis={
            "range": [0, 10.5],
            "gridcolor": PALETA["borda"],
        },
        legend={
            "bgcolor": "rgba(0,0,0,0)",
            "bordercolor": PALETA["borda"],
        },
    )
    return figura


def grafico_radar_aluno(
    indicadores: dict,
) -> go.Figure:
    categorias = [
        "Frequência",
        "Nota de provas",
        "Nota de atividades",
        "Participação",
        "Taxa de exercícios",
    ]
    valores = [
        min(indicadores["frequencia"] / 10, 10),
        indicadores["nota_provas"],
        indicadores["nota_atividades"],
        indicadores["participacao"],
        min(
            indicadores["taxa_exercicios"] / 10,
            10,
        ),
    ]

    figura = go.Figure(
        go.Scatterpolar(
            r=valores + [valores[0]],
            theta=categorias + [categorias[0]],
            fill="toself",
            fillcolor="rgba(91, 141, 239, 0.15)",
            line={
                "color": PALETA["destaque"],
                "width": 2,
            },
            marker={"size": 6},
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
                "color": PALETA[
                    "texto_secundario"
                ],
            },
            "angularaxis": {
                "gridcolor": PALETA["borda"],
                "color": PALETA[
                    "texto_primario"
                ],
            },
        },
        font={
            "family": "Arial, sans-serif",
            "color": PALETA["texto_primario"],
            "size": 13,
        },
        margin={
            "l": 40,
            "r": 40,
            "t": 40,
            "b": 40,
        },
        title={
            "text": "Perfil dos indicadores",
            "font": {"size": 15},
        },
        showlegend=False,
    )
    return figura


def grafico_comparativo_turma(
    dataframe: pd.DataFrame,
) -> go.Figure:
    dados = dataframe.dropna(
        subset=["Nota Provas"]
    ).copy()
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
            x=dados["Aluno"],
            y=dados["Nota Provas"],
            marker_color=cores.tolist(),
            text=dados["Nota Provas"].round(1),
            textposition="outside",
        )
    )
    figura.update_layout(
        **LAYOUT_BASE,
        title={
            "text": "Nota de provas por aluno",
            "font": {"size": 15},
        },
        yaxis_title="Nota (0–10)",
        yaxis={
            "range": [0, 11],
            "gridcolor": PALETA["borda"],
        },
        xaxis={
            "tickangle": -30,
            "gridcolor": PALETA["borda"],
        },
        showlegend=False,
    )
    return figura
