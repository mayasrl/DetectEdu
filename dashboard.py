import pandas as pd
import streamlit as st

import analytics
import charts
import repository as repo
from models import CLASSIFICACAO_CORES, CLASSIFICACAO_LABELS


def _metric_card(label: str, value: str, sublabel: str = "") -> None:
    st.html(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sublabel">{sublabel}</div>
        </div>
        """
    )


def pagina_dashboard() -> None:
    st.header("Dashboard analítico")
    st.caption(
        "Visão consolidada da turma para apoiar a priorização do acompanhamento pedagógico."
    )

    turmas = repo.listar_turmas()
    if not turmas:
        st.info("Nenhuma turma cadastrada. Acesse a página de turmas para começar.")
        return

    opcoes_turma = {
        f"{turma['nome_turma']} — {turma['disciplina']} ({turma['semestre']})": turma["id"]
        for turma in turmas
    }
    turma_selecionada = st.selectbox(
        "Turma",
        list(opcoes_turma),
        key="dashboard_turma",
    )
    turma_id = opcoes_turma[turma_selecionada]

    dataframe = analytics.construir_dataframe_turma(turma_id)
    metricas = analytics.calcular_metricas_turma(dataframe)

    if not metricas:
        st.info("Nenhum aluno com acompanhamento nesta turma.")
        _tabela_alunos(dataframe)
        return

    st.subheader("Resumo da turma")
    resumo = st.columns(4)

    with resumo[0]:
        _metric_card(
            "Alunos acompanhados",
            str(metricas["com_dados"]),
            f"{metricas['total_alunos']} cadastrados",
        )

    with resumo[1]:
        _metric_card(
            "Frequência média",
            f"{metricas['media_frequencia']:.1f}%",
            "último registro",
        )

    with resumo[2]:
        _metric_card(
            "Média de provas",
            f"{metricas['media_nota_provas']:.1f}",
            "escala de 0 a 10",
        )

    with resumo[3]:
        _metric_card(
            "Prioridade de acompanhamento",
            str(metricas["intervencao"]),
            "alunos",
        )

    st.subheader("Panorama analítico")
    grafico_esquerda, grafico_direita = st.columns([0.9, 1.4])

    with grafico_esquerda:
        st.plotly_chart(
            charts.grafico_distribuicao_classificacao(metricas),
            use_container_width=True,
        )

    with grafico_direita:
        st.plotly_chart(
            charts.grafico_dispersao_frequencia_nota(dataframe),
            use_container_width=True,
        )

    grafico_esquerda, grafico_direita = st.columns(2)

    with grafico_esquerda:
        st.plotly_chart(
            charts.grafico_medias_turma(dataframe),
            use_container_width=True,
        )

    with grafico_direita:
        st.plotly_chart(
            charts.grafico_comparativo_turma(dataframe),
            use_container_width=True,
        )

    st.divider()
    st.subheader("Visão da turma")
    _tabela_alunos(dataframe)

    st.divider()
    _painel_individual(turma_id)


def _tabela_alunos(dataframe: pd.DataFrame) -> None:
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
        "Ativ. Entregues",
        "Ativ. Atrasadas",
        "Classificação",
    ]
    tabela = dataframe[colunas].copy()

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Frequência (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Nota Provas": st.column_config.NumberColumn(format="%.2f"),
            "Nota Atividades": st.column_config.NumberColumn(format="%.2f"),
            "Taxa Exercícios (%)": st.column_config.NumberColumn(format="%.1f%%"),
        },
    )


def _painel_individual(turma_id: int) -> None:
    st.subheader("Análise individual")
    st.caption(
        "Selecione um aluno para visualizar os indicadores do último registro e sua evolução."
    )

    alunos = repo.listar_alunos(turma_id)
    if not alunos:
        return

    opcoes_aluno = {
        f"{aluno['nome_aluno']} ({aluno['matricula']})": aluno["id"]
        for aluno in alunos
    }
    aluno_selecionado = st.selectbox(
        "Selecionar aluno",
        list(opcoes_aluno),
        key="dashboard_aluno",
    )
    aluno_id = opcoes_aluno[aluno_selecionado]

    indicadores = analytics.calcular_indicadores_aluno(aluno_id)
    if indicadores is None:
        st.info("Nenhum acompanhamento registrado para este aluno.")
        return

    chave = indicadores["classificacao"]
    cor = CLASSIFICACAO_CORES[chave]
    classificacao = CLASSIFICACAO_LABELS[chave]

    st.html(
        f"""
        <div class="classification-card" style="--classification-color:{cor}">
            <div class="classification-eyebrow">
                Último registro: {indicadores['ultimo_registro']}
            </div>
            <div class="classification-title">{classificacao}</div>
            <div class="classification-score">
                Pontuação atual: <strong>{indicadores['pontuacao']}</strong>
            </div>
        </div>
        """
    )

    metricas = st.columns(3)

    with metricas[0]:
        _metric_card("Frequência", f"{indicadores['frequencia']}%")
        _metric_card("Nota de provas", f"{indicadores['nota_provas']:.2f}")

    with metricas[1]:
        _metric_card("Nota de atividades", f"{indicadores['nota_atividades']:.2f}")
        _metric_card("Participação", f"{indicadores['participacao']:.1f} / 10")

    with metricas[2]:
        taxa_exercicios = (
            f"{indicadores['taxa_exercicios']}%"
            if indicadores["taxa_exercicios"] is not None
            else "Não aplicável"
        )
        _metric_card("Taxa de exercícios", taxa_exercicios)

        nomes_evolucao = {
            "positiva": "Melhora",
            "estavel": "Sem variação relevante",
            "negativa": "Queda",
            "sem_historico": "Sem histórico",
        }
        _metric_card(
            "Evolução das notas",
            nomes_evolucao.get(indicadores["evolucao"], indicadores["evolucao"]),
        )

    st.caption(
        f"Atividades entregues no período: {indicadores['atividades_entregues']} · "
        f"Atividades atrasadas: {indicadores['atividades_atrasadas']}"
    )

    info_esquerda, info_direita = st.columns(2)

    with info_esquerda:
        st.markdown("### Fatores de atenção")
        if indicadores["fatores_atencao"]:
            for fator in indicadores["fatores_atencao"]:
                st.markdown(f"- {fator}")
        else:
            st.markdown("Nenhum fator de atenção no último registro.")

    with info_direita:
        st.markdown("### Sugestões de acompanhamento")
        if indicadores["recomendacoes"]:
            for recomendacao in indicadores["recomendacoes"]:
                st.markdown(f"- {recomendacao}")
        else:
            st.markdown("Manter o acompanhamento regular do aluno.")

    grafico_radar, grafico_evolucao = st.columns(2)
    serie_temporal = analytics.construir_serie_temporal_aluno(aluno_id)

    with grafico_radar:
        st.plotly_chart(
            charts.grafico_radar_aluno(indicadores),
            use_container_width=True,
        )

    with grafico_evolucao:
        st.plotly_chart(
            charts.grafico_evolucao_aluno(serie_temporal),
            use_container_width=True,
        )
