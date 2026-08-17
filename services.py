def dividir(
    numerador: float,
    denominador: float,
    valor_padrao: float = 0.0,
) -> float:
    if denominador == 0:
        return valor_padrao

    return numerador / denominador


def calcular_frequencia(
    aulas_dadas: int,
    faltas: int,
) -> float:
    presencas = aulas_dadas - faltas
    return dividir(presencas, aulas_dadas) * 100


def calcular_nota_padronizada(
    nota_obtida: float,
    nota_maxima: float,
) -> float:
    return dividir(nota_obtida, nota_maxima) * 10


def calcular_taxa_exercicios(
    resolvidos: int,
    propostos: int,
) -> float | None:
    if propostos == 0:
        return None

    return dividir(resolvidos, propostos) * 100


def calcular_media_desempenho(
    nota_provas: float,
    nota_atividades: float,
) -> float:
    return (nota_provas + nota_atividades) / 2


def calcular_evolucao(
    media_atual: float,
    media_anterior: float | None,
) -> str:
    if media_anterior is None:
        return "sem_historico"

    diferenca = media_atual - media_anterior

    if diferenca > 0.5:
        return "positiva"

    if diferenca < -0.5:
        return "negativa"

    return "estavel"


def _pontos_frequencia(frequencia: float) -> int:
    if frequencia >= 85:
        return 0

    if frequencia >= 75:
        return 1

    return 2


def _pontos_nota(nota: float) -> int:
    if nota >= 7:
        return 0

    if nota >= 6:
        return 1

    return 2


def _pontos_atividades_atrasadas(
    atividades_atrasadas: int,
) -> int:
    if atividades_atrasadas <= 1:
        return 0

    if atividades_atrasadas <= 3:
        return 1

    return 2


def _pontos_participacao(
    participacao: float,
) -> int:
    if participacao >= 7:
        return 0

    if participacao >= 5:
        return 1

    return 2


def _pontos_exercicios(
    taxa_exercicios: float | None,
) -> int:
    if taxa_exercicios is None:
        return 0

    if taxa_exercicios >= 80:
        return 0

    if taxa_exercicios >= 60:
        return 1

    return 2


def _pontos_evolucao(evolucao: str) -> int:
    if evolucao in {"positiva", "estavel", "sem_historico"}:
        return 0

    return 2


def classificar_aluno(
    frequencia: float,
    nota_provas: float,
    nota_atividades: float,
    atividades_atrasadas: int,
    participacao: float,
    taxa_exercicios: float | None,
    evolucao: str,
) -> tuple[str, int, dict[str, int]]:
    pontos_por_indicador = {
        "Frequência": _pontos_frequencia(frequencia),
        "Nota de provas": _pontos_nota(nota_provas),
        "Nota de atividades": _pontos_nota(nota_atividades),
        "Atividades atrasadas": _pontos_atividades_atrasadas(
            atividades_atrasadas
        ),
        "Participação em aula": _pontos_participacao(
            participacao
        ),
        "Taxa de exercícios": _pontos_exercicios(
            taxa_exercicios
        ),
        "Evolução das notas": _pontos_evolucao(
            evolucao
        ),
    }

    pontuacao = sum(pontos_por_indicador.values())

    if pontuacao <= 3:
        classificacao = "sem_indicios"
    elif pontuacao <= 7:
        classificacao = "atencao"
    else:
        classificacao = "intervencao"

    return classificacao, pontuacao, pontos_por_indicador


def fatores_de_atencao(
    pontos_por_indicador: dict[str, int],
) -> list[str]:
    return [
        indicador
        for indicador, pontos in pontos_por_indicador.items()
        if pontos > 0
    ]


def gerar_recomendacoes(
    pontos_por_indicador: dict[str, int],
) -> list[str]:
    recomendacoes: list[str] = []

    if pontos_por_indicador.get("Frequência", 0) > 0:
        recomendacoes.append(
            "Verificar as causas das ausências e acompanhar a frequência."
        )

    if pontos_por_indicador.get("Nota de provas", 0) > 0:
        recomendacoes.append(
            "Revisar os conteúdos com menor desempenho nas avaliações."
        )

    if pontos_por_indicador.get("Nota de atividades", 0) > 0:
        recomendacoes.append(
            "Observar as dificuldades apresentadas nas atividades."
        )

    if pontos_por_indicador.get("Atividades atrasadas", 0) > 0:
        recomendacoes.append(
            "Acompanhar os prazos e verificar dificuldades de organização."
        )

    if pontos_por_indicador.get("Participação em aula", 0) > 0:
        recomendacoes.append(
            "Propor estratégias para ampliar a participação em aula."
        )

    if pontos_por_indicador.get("Taxa de exercícios", 0) > 0:
        recomendacoes.append(
            "Reforçar a prática dos conteúdos por meio de exercícios."
        )

    if pontos_por_indicador.get("Evolução das notas", 0) > 0:
        recomendacoes.append(
            "Acompanhar a evolução nas próximas avaliações."
        )

    return recomendacoes
