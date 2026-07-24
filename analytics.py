import pandas as pd

import repository as repo
import services as svc
from models import CLASSIFICACAO_LABELS


def _media_registro(registro) -> float:
    nota_provas = svc.calcular_nota_padronizada(
        registro["nota_provas_obtida"],
        registro["nota_provas_maxima"],
    )
    nota_atividades = svc.calcular_nota_padronizada(
        registro["nota_atividades_obtida"],
        registro["nota_atividades_maxima"],
    )
    return svc.calcular_media_desempenho(
        nota_provas,
        nota_atividades,
    )


def _calcular_indicadores(
    registro,
    registro_anterior=None,
) -> dict:
    frequencia = svc.calcular_frequencia(
        registro["aulas_dadas"],
        registro["faltas"],
    )
    nota_provas = svc.calcular_nota_padronizada(
        registro["nota_provas_obtida"],
        registro["nota_provas_maxima"],
    )
    nota_atividades = svc.calcular_nota_padronizada(
        registro["nota_atividades_obtida"],
        registro["nota_atividades_maxima"],
    )
    taxa_exercicios = svc.calcular_taxa_exercicios(
        registro["exercicios_resolvidos"],
        registro["exercicios_propostos"],
    )

    media_anterior = None
    if registro_anterior is not None:
        media_anterior = _media_registro(registro_anterior)

    media_atual = svc.calcular_media_desempenho(
        nota_provas,
        nota_atividades,
    )
    evolucao = svc.calcular_evolucao(
        media_atual,
        media_anterior,
    )

    return {
        "frequencia": frequencia,
        "nota_provas": nota_provas,
        "nota_atividades": nota_atividades,
        "taxa_exercicios": taxa_exercicios,
        "evolucao": evolucao,
    }


def construir_dataframe_turma(
    turma_id: int,
) -> pd.DataFrame:
    alunos = repo.listar_alunos(turma_id)
    registros: list[dict] = []

    for aluno in alunos:
        ultimo = repo.ultimo_acompanhamento(aluno["id"])
        penultimo = repo.penultimo_acompanhamento(aluno["id"])

        if ultimo is None:
            registros.append(
                {
                    "id": aluno["id"],
                    "Aluno": aluno["nome_aluno"],
                    "Matrícula": aluno["matricula"],
                    "Frequência (%)": None,
                    "Nota Provas": None,
                    "Nota Atividades": None,
                    "Ativ. Atrasadas": None,
                    "Participação": None,
                    "Taxa Exercícios (%)": None,
                    "Evolução": None,
                    "Pontuação": None,
                    "Classificação": "Sem registros",
                    "classificacao_key": None,
                }
            )
            continue

        indicadores = _calcular_indicadores(
            ultimo,
            penultimo,
        )
        classificacao, pontuacao, _ = svc.classificar_aluno(
            indicadores["frequencia"],
            indicadores["nota_provas"],
            indicadores["nota_atividades"],
            ultimo["atividades_atrasadas"],
            ultimo["participacao_aula"],
            indicadores["taxa_exercicios"],
            indicadores["evolucao"],
        )

        registros.append(
            {
                "id": aluno["id"],
                "Aluno": aluno["nome_aluno"],
                "Matrícula": aluno["matricula"],
                "Frequência (%)": round(
                    indicadores["frequencia"],
                    1,
                ),
                "Nota Provas": round(
                    indicadores["nota_provas"],
                    2,
                ),
                "Nota Atividades": round(
                    indicadores["nota_atividades"],
                    2,
                ),
                "Ativ. Atrasadas": ultimo["atividades_atrasadas"],
                "Participação": ultimo["participacao_aula"],
                "Taxa Exercícios (%)": round(
                    indicadores["taxa_exercicios"],
                    1,
                ),
                "Evolução": indicadores["evolucao"],
                "Pontuação": pontuacao,
                "Classificação": CLASSIFICACAO_LABELS[
                    classificacao
                ],
                "classificacao_key": classificacao,
            }
        )

    return pd.DataFrame(registros)


def construir_serie_temporal_aluno(
    aluno_id: int,
) -> pd.DataFrame:
    acompanhamentos = repo.listar_acompanhamentos(
        aluno_id
    )
    if not acompanhamentos:
        return pd.DataFrame()

    registros: list[dict] = []
    anterior = None

    for acompanhamento in acompanhamentos:
        indicadores = _calcular_indicadores(
            acompanhamento,
            anterior,
        )

        registros.append(
            {
                "Data": acompanhamento["data_registro"],
                "Frequência (%)": round(
                    indicadores["frequencia"],
                    1,
                ),
                "Nota Provas": round(
                    indicadores["nota_provas"],
                    2,
                ),
                "Nota Atividades": round(
                    indicadores["nota_atividades"],
                    2,
                ),
                "Participação": acompanhamento[
                    "participacao_aula"
                ],
                "Taxa Exercícios (%)": round(
                    indicadores["taxa_exercicios"],
                    1,
                ),
                "Evolução": indicadores["evolucao"],
                "acompanhamento_id": acompanhamento["id"],
            }
        )
        anterior = acompanhamento

    dataframe = pd.DataFrame(registros)
    dataframe["Data"] = pd.to_datetime(
        dataframe["Data"]
    )
    return dataframe.sort_values("Data")


def calcular_metricas_turma(
    dataframe: pd.DataFrame,
) -> dict:
    com_dados = dataframe.dropna(
        subset=["Frequência (%)"]
    )
    if com_dados.empty:
        return {}

    return {
        "total_alunos": len(dataframe),
        "com_dados": len(com_dados),
        "sem_indicios": (
            com_dados["classificacao_key"] == "sem_indicios"
        ).sum(),
        "atencao": (
            com_dados["classificacao_key"] == "atencao"
        ).sum(),
        "intervencao": (
            com_dados["classificacao_key"] == "intervencao"
        ).sum(),
        "media_frequencia": com_dados[
            "Frequência (%)"
        ].mean(),
        "media_nota_provas": com_dados[
            "Nota Provas"
        ].mean(),
        "media_nota_atividades": com_dados[
            "Nota Atividades"
        ].mean(),
        "media_taxa_exercicios": com_dados[
            "Taxa Exercícios (%)"
        ].mean(),
    }


def calcular_indicadores_aluno(
    aluno_id: int,
) -> dict | None:
    ultimo = repo.ultimo_acompanhamento(aluno_id)
    penultimo = repo.penultimo_acompanhamento(aluno_id)

    if ultimo is None:
        return None

    indicadores = _calcular_indicadores(
        ultimo,
        penultimo,
    )
    classificacao, pontuacao, pontos = svc.classificar_aluno(
        indicadores["frequencia"],
        indicadores["nota_provas"],
        indicadores["nota_atividades"],
        ultimo["atividades_atrasadas"],
        ultimo["participacao_aula"],
        indicadores["taxa_exercicios"],
        indicadores["evolucao"],
    )

    return {
        "frequencia": round(
            indicadores["frequencia"],
            1,
        ),
        "nota_provas": round(
            indicadores["nota_provas"],
            2,
        ),
        "nota_atividades": round(
            indicadores["nota_atividades"],
            2,
        ),
        "atividades_atrasadas": ultimo[
            "atividades_atrasadas"
        ],
        "participacao": ultimo["participacao_aula"],
        "taxa_exercicios": round(
            indicadores["taxa_exercicios"],
            1,
        ),
        "evolucao": indicadores["evolucao"],
        "classificacao": classificacao,
        "pontuacao": pontuacao,
        "pontos_por_indicador": pontos,
        "fatores_atencao": svc.fatores_de_atencao(
            pontos
        ),
        "recomendacoes": svc.gerar_recomendacoes(
            pontos
        ),
        "ultimo_registro": ultimo["data_registro"],
    }
