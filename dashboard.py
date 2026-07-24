import pandas as pd
import streamlit as st

import analytics
import charts
import repository as repo
from models import (
    CLASSIFICACAO_CORES,
    CLASSIFICACAO_LABELS,
)


def _metric_card(
    label: str,
    value: str,
    sublabel: str = "",
) -> None:
    st.markdown(
        f"""
        <div style="
            background:#1A1D27;
            border:1px solid #2A2D3E;
            border-radius:8px;
            padding:16px 20px;
            margin-bottom:4px;
        ">
            <div style="
                color:#9BA3BB;
                font-size:12px;
                text-transform:uppercase;
                letter-spacing:.06em;
            ">
                {label}
            </div>
            <div style="
                color:#E8EAF0;
                font-size:26px;
                font-weight:600;
                margin:4px 0;
            ">
                {value}
            </div>
            <div style="
                color:#9BA3BB;
                font-size:12px;
            ">
                {sublabel}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pagina_dashboard() -> None:
    st.header("Dashboard analítico")

    turmas = repo.listar_turmas()
    if not turmas:
        st.info(
            "Nenhuma turma cadastrada. "
            "Acesse a página de turmas para começar."
        )
        return

    opcoes_turma = {
        (
            f"{turma['nome_turma']} — "
            f"{turma['disciplina']} "
            f"({turma['semestre']})"
        ): turma["id"]
        for turma in turmas
    }
    turma_selecionada = st.selectbox(
        "Turma",
        list(opcoes_turma),
        key="dashboard_turma",
    )
    turma_id = opcoes_turma[turma_selecionada]

    dataframe = analytics.construir_dataframe_turma(
        turma_id
    )
    metricas = analytics.calcular_metricas_turma(
        dataframe
    )

    if not metricas:
        st.info(
            "Nenhum aluno com acompanhamento nesta turma."
        )
        _tabela_alunos(dataframe)
        return

    colunas = st.columns(5)

    with colunas[0]:
        _metric_card(
            "Total de alunos",
            str(metricas["total_alunos"]),
            f"{metricas['com_dados']} com registros",
        )

    with colunas[1]:
        _metric_card(
            "Sem indícios",
            str(metricas["sem_indicios"]),
            "alunos",
        )

    with colunas[2]:
        _metric_card(
            "Atenção pedagógica",
            str(metricas["atencao"]),
            "alunos",
        )

    with colunas[3]:
        _metric_card(
            "Necessita intervenção",
            str(metricas["intervencao"]),
            "alunos",
        )

    with colunas[4]:
        _metric_card(
            "Frequência média",
            f"{metricas['media_frequencia']:.1f}%",
        )

    st.divider()

    grafico_esquerda, grafico_direita = st.columns(2)

    with grafico_esquerda:
        st.plotly_chart(
            charts.grafico_distribuicao_classificacao(
                metricas
            ),
            use_container_width=True,
        )

    with grafico_direita:
        st.plotly_chart(
            charts.grafico_dispersao_frequencia_nota(
                dataframe
            ),
            use_container_width=True,
        )

    st.plotly_chart(
        charts.grafico_comparativo_turma(dataframe),
        use_container_width=True,
    )

    st.divider()
    st.subheader("Visão da turma")
    _tabela_alunos(dataframe)

    st.divider()
    _painel_individual(turma_id)


def _tabela_alunos(
    dataframe: pd.DataFrame,
) -> None:
    if dataframe.empty:
        st.info("Nenhum aluno cadastrado.")
        return

    colunas = [
        "Aluno",
        "Matrícula",
        "Frequência (%)",
        "Nota Provas",
        "Nota Atividades",
        "Taxa Exercícios (%)",
        "Ativ. Atrasadas",
        "Classificação",
    ]
    tabela = dataframe[colunas].copy()

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Frequência (%)": st.column_config.NumberColumn(
                format="%.1f%%"
            ),
            "Nota Provas": st.column_config.NumberColumn(
                format="%.2f"
            ),
            "Nota Atividades": st.column_config.NumberColumn(
                format="%.2f"
            ),
            "Taxa Exercícios (%)": (
                st.column_config.NumberColumn(
                    format="%.1f%%"
                )
            ),
        },
    )


def _painel_individual(
    turma_id: int,
) -> None:
    st.subheader("Análise individual")

    alunos = repo.listar_alunos(turma_id)
    if not alunos:
        return

    opcoes_aluno = {
        (
            f"{aluno['nome_aluno']} "
            f"({aluno['matricula']})"
        ): aluno["id"]
        for aluno in alunos
    }
    aluno_selecionado = st.selectbox(
        "Selecionar aluno",
        list(opcoes_aluno),
        key="dashboard_aluno",
    )
    aluno_id = opcoes_aluno[aluno_selecionado]

    indicadores = analytics.calcular_indicadores_aluno(
        aluno_id
    )
    if indicadores is None:
        st.info(
            "Nenhum acompanhamento registrado para este aluno."
        )
        return

    chave = indicadores["classificacao"]
    cor = CLASSIFICACAO_CORES[chave]
    classificacao = CLASSIFICACAO_LABELS[chave]

    st.markdown(
        f"""
        <div style="
            background:#1A1D27;
            border:1px solid {cor}55;
            border-left:4px solid {cor};
            border-radius:8px;
            padding:16px 20px;
            margin-bottom:16px;
        ">
            <div style="
                color:#9BA3BB;
                font-size:12px;
                text-transform:uppercase;
                letter-spacing:.06em;
            ">
                Classificação pedagógica ·
                Último registro:
                {indicadores['ultimo_registro']}
            </div>
            <div style="
                color:{cor};
                font-size:22px;
                font-weight:600;
                margin:6px 0;
            ">
                {classificacao}
            </div>
            <div style="
                color:#9BA3BB;
                font-size:13px;
            ">
                Pontuação:
                {indicadores['pontuacao']} / 14
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    colunas = st.columns(3)

    with colunas[0]:
        _metric_card(
            "Frequência",
            f"{indicadores['frequencia']}%",
        )
        _metric_card(
            "Nota de provas",
            f"{indicadores['nota_provas']:.2f}",
        )

    with colunas[1]:
        _metric_card(
            "Nota de atividades",
            f"{indicadores['nota_atividades']:.2f}",
        )
        _metric_card(
            "Participação",
            f"{indicadores['participacao']:.1f} / 10",
        )

    with colunas[2]:
        _metric_card(
            "Taxa de exercícios",
            f"{indicadores['taxa_exercicios']}%",
        )
        evolucao = indicadores["evolucao"].replace(
            "_",
            " ",
        ).capitalize()
        _metric_card(
            "Evolução das notas",
            evolucao,
        )

    if indicadores["fatores_atencao"]:
        st.markdown("**Fatores de atenção**")
        for fator in indicadores["fatores_atencao"]:
            st.write(f"• {fator}")

    if indicadores["recomendacoes"]:
        st.markdown("**Sugestões de acompanhamento**")
        for recomendacao in indicadores["recomendacoes"]:
            st.write(f"• {recomendacao}")

    grafico_radar, grafico_evolucao = st.columns(2)
    serie_temporal = (
        analytics.construir_serie_temporal_aluno(
            aluno_id
        )
    )

    with grafico_radar:
        st.plotly_chart(
            charts.grafico_radar_aluno(indicadores),
            use_container_width=True,
        )

    with grafico_evolucao:
        st.plotly_chart(
            charts.grafico_evolucao_aluno(
                serie_temporal
            ),
            use_container_width=True,
        )
