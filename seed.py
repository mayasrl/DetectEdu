from datetime import date

import repository as repo
from models import Acompanhamento, Aluno, Turma


DATAS = [
    date(2026, 3, 10),
    date(2026, 4, 10),
    date(2026, 5, 10),
    date(2026, 6, 10),
]


def registro(
    frequencia: int,
    prova: float,
    atividade: float,
    atrasos: int,
    participacao: float,
    exercicios: int | None,
) -> dict:
    return {
        "frequencia": frequencia,
        "prova": prova,
        "atividade": atividade,
        "atrasos": atrasos,
        "participacao": participacao,
        "exercicios": exercicios,
    }


PERFIS = {
    "consistente": [
        registro(90, 8.0, 8.2, 0, 8.0, 90),
        registro(90, 8.1, 8.0, 0, 8.0, 90),
        registro(95, 8.3, 8.4, 0, 8.5, 95),
        registro(90, 8.2, 8.5, 0, 8.5, 90),
    ],
    "melhora": [
        registro(80, 5.8, 5.7, 3, 5.5, 65),
        registro(85, 6.4, 6.5, 2, 6.0, 70),
        registro(90, 7.4, 7.5, 1, 7.0, 85),
        registro(95, 8.0, 8.2, 0, 8.0, 90),
    ],
    "exercicios_na": [
        registro(90, 7.8, 8.0, 1, 7.5, None),
        registro(90, 8.0, 8.0, 0, 8.0, None),
        registro(95, 8.2, 8.1, 0, 8.0, None),
        registro(95, 8.1, 8.3, 0, 8.5, None),
    ],
    "limiar_regular": [
        registro(80, 6.5, 6.5, 0, 7.0, 80),
        registro(80, 6.5, 6.5, 0, 7.0, 80),
        registro(80, 6.5, 6.5, 0, 7.0, 80),
        registro(80, 6.5, 6.5, 0, 7.0, 80),
    ],
    "baixa_frequencia": [
        registro(70, 7.5, 7.4, 2, 7.0, 70),
        registro(70, 7.6, 7.5, 2, 7.0, 70),
        registro(70, 7.7, 7.6, 2, 7.5, 70),
        registro(70, 7.6, 7.7, 2, 7.5, 70),
    ],
    "notas_baixas": [
        registro(90, 5.2, 5.4, 0, 7.5, 85),
        registro(90, 5.3, 5.5, 0, 7.5, 85),
        registro(90, 5.4, 5.6, 0, 7.0, 85),
        registro(90, 5.5, 5.7, 0, 7.0, 85),
    ],
    "baixa_participacao": [
        registro(85, 7.2, 7.0, 2, 4.5, 70),
        registro(85, 7.3, 7.1, 2, 4.5, 70),
        registro(90, 7.3, 7.2, 2, 4.0, 70),
        registro(90, 7.4, 7.3, 2, 4.0, 70),
    ],
    "atrasos": [
        registro(85, 7.2, 7.0, 4, 6.0, 70),
        registro(85, 7.3, 7.1, 4, 6.0, 70),
        registro(90, 7.4, 7.2, 5, 6.0, 70),
        registro(90, 7.5, 7.3, 5, 6.0, 70),
    ],
    "notas_altas_freq_baixa": [
        registro(70, 8.0, 8.2, 2, 7.5, 70),
        registro(70, 8.2, 8.1, 2, 7.5, 70),
        registro(70, 8.1, 8.3, 2, 8.0, 70),
        registro(70, 8.3, 8.4, 2, 8.0, 70),
    ],
    "freq_alta_notas_baixas": [
        registro(95, 5.2, 5.4, 0, 8.0, 90),
        registro(95, 5.3, 5.5, 0, 8.0, 90),
        registro(95, 5.4, 5.6, 0, 8.0, 90),
        registro(95, 5.5, 5.7, 0, 8.0, 90),
    ],
    "limiar_atencao": [
        registro(80, 6.5, 6.5, 0, 6.0, 80),
        registro(80, 6.5, 6.5, 0, 6.0, 80),
        registro(80, 6.5, 6.5, 0, 6.0, 80),
        registro(80, 6.5, 6.5, 0, 6.0, 80),
    ],
    "queda": [
        registro(90, 8.2, 8.0, 0, 8.0, 90),
        registro(85, 7.2, 7.0, 1, 7.0, 80),
        registro(80, 5.8, 5.6, 2, 6.0, 70),
        registro(75, 5.2, 5.0, 4, 4.5, 55),
    ],
    "multiplos_moderados": [
        registro(90, 8.0, 7.8, 0, 8.0, 90),
        registro(85, 7.4, 7.3, 1, 7.0, 80),
        registro(80, 6.7, 6.6, 2, 6.0, 70),
        registro(75, 6.0, 6.0, 3, 5.0, 60),
    ],
    "critico": [
        registro(75, 6.0, 6.2, 3, 5.0, 60),
        registro(70, 5.5, 5.6, 4, 4.5, 55),
        registro(65, 5.0, 5.2, 5, 4.0, 50),
        registro(60, 4.5, 4.8, 6, 3.5, 45),
    ],
    "limiar_prioridade": [
        registro(70, 6.5, 6.5, 4, 6.0, 70),
        registro(70, 6.5, 6.5, 4, 6.0, 70),
        registro(70, 6.5, 6.5, 4, 6.0, 70),
        registro(70, 6.5, 6.5, 4, 6.0, 70),
    ],
}


TURMAS = [
    {
        "turma": Turma(
            nome_turma="1º Ano A - Manhã",
            curso="Ensino Médio",
            disciplina="Matemática",
            semestre="2026.1",
            professor="Marina Lopes",
        ),
        "matricula_inicio": 20261001,
        "alunos": [
            ("Lucas Ferreira", "consistente", 1),
            ("Mariana Souza", "exercicios_na", 1),
            ("Felipe Alves", "limiar_regular", 1),
            ("Beatriz Costa", "consistente", 2),
            ("Rafael Mendes", "limiar_regular", 2),
            ("Amanda Oliveira", "exercicios_na", 2),
            ("Thiago Santos", "consistente", 2),
            ("Larissa Pereira", "limiar_regular", 2),
            ("Gabriel Rocha", "consistente", 2),
            ("Júlia Martins", "consistente", 2),
            ("Vinícius Carvalho", "melhora", 3),
            ("Camila Nunes", "melhora", 3),
            ("Henrique Ribeiro", "melhora", 4),
            ("Isabela Freitas", "baixa_frequencia", 3),
            ("Matheus Barbosa", "notas_baixas", 3),
            ("Sofia Almeida", "baixa_participacao", 3),
            ("Bruno Teixeira", "atrasos", 3),
            ("Letícia Cardoso", "notas_altas_freq_baixa", 3),
            ("Gustavo Moreira", "freq_alta_notas_baixas", 3),
            ("Ana Clara Lopes", "limiar_atencao", 3),
            ("Daniel Azevedo", "baixa_frequencia", 4),
            ("Luana Castro", "queda", 3),
            ("Caio Fernandes", "multiplos_moderados", 3),
            ("Vitória Moraes", "critico", 4),
            ("André Lima", "limiar_prioridade", 3),
        ],
    },
    {
        "turma": Turma(
            nome_turma="1º Ano B - Manhã",
            curso="Ensino Médio",
            disciplina="Matemática",
            semestre="2026.1",
            professor="Marina Lopes",
        ),
        "matricula_inicio": 20262001,
        "alunos": [
            ("João Victor Lima", "consistente", 1),
            ("Carolina Ramos", "exercicios_na", 1),
            ("Eduardo Barros", "limiar_regular", 1),
            ("Natália Gomes", "consistente", 2),
            ("Pedro Henrique Silva", "exercicios_na", 2),
            ("Bianca Moura", "limiar_regular", 2),
            ("Leonardo Pires", "consistente", 2),
            ("Yasmin Correia", "limiar_regular", 2),
            ("Miguel Araújo", "consistente", 2),
            ("Helena Duarte", "limiar_regular", 2),
            ("Arthur Monteiro", "consistente", 2),
            ("Manuela Reis", "melhora", 3),
            ("Enzo Vieira", "baixa_frequencia", 3),
            ("Laura Campos", "notas_baixas", 3),
            ("Samuel Cunha", "baixa_participacao", 3),
            ("Alice Farias", "atrasos", 3),
            ("Davi Peixoto", "notas_altas_freq_baixa", 3),
            ("Lívia Neves", "freq_alta_notas_baixas", 3),
            ("Murilo Andrade", "limiar_atencao", 3),
            ("Cecília Tavares", "baixa_frequencia", 3),
            ("Nicolas Prado", "notas_baixas", 3),
            ("Maitê Guimarães", "baixa_participacao", 3),
            ("Igor Batista", "atrasos", 3),
            ("Heloísa Rezende", "queda", 3),
            ("Bernardo Viana", "multiplos_moderados", 3),
            ("Lorena Siqueira", "critico", 3),
            ("Otávio Coelho", "limiar_prioridade", 4),
            ("Eloá Macedo", "queda", 4),
            ("Wesley Braga", "multiplos_moderados", 4),
            ("Rebeca Assis", "critico", 4),
        ],
    },
    {
        "turma": Turma(
            nome_turma="2º Ano A - Tarde",
            curso="Ensino Médio",
            disciplina="Matemática",
            semestre="2026.1",
            professor="Marina Lopes",
        ),
        "matricula_inicio": 20263001,
        "alunos": [
            ("Alexandre Melo", "consistente", 1),
            ("Clara Pontes", "exercicios_na", 1),
            ("Guilherme Borges", "limiar_regular", 2),
            ("Melissa Xavier", "consistente", 2),
            ("Vitor Hugo Dias", "exercicios_na", 2),
            ("Sarah Paiva", "limiar_regular", 2),
            ("Heitor Fonseca", "consistente", 2),
            ("Nicole Guerra", "melhora", 3),
            ("Renan Leal", "melhora", 3),
            ("Gabriela Pacheco", "consistente", 3),
            ("João Pedro Matos", "limiar_regular", 3),
            ("Maria Eduarda Sales", "baixa_frequencia", 3),
            ("Erick Cavalcante", "notas_baixas", 3),
            ("Brenda Rios", "baixa_participacao", 3),
            ("Alan Queiroz", "atrasos", 3),
            ("Fernanda Lacerda", "notas_altas_freq_baixa", 3),
            ("Luiz Felipe Mota", "queda", 4),
            ("Tainá Soares", "critico", 4),
            ("Paulo César Dantas", "multiplos_moderados", 4),
        ],
    },
]


AJUSTES_ULTIMO_REGISTRO = {"Mariana Souza": {"atrasos": 2},
 "Beatriz Costa": {"atrasos": 2},
 "Rafael Mendes": {"frequencia": 90},
 "Thiago Santos": {"exercicios": 50},
 "Gabriel Rocha": {"exercicios": 50},
 "Vinícius Carvalho": {"atrasos": 2},
 "Henrique Ribeiro": {"atrasos": 2},
 "Matheus Barbosa": {"participacao": 4.5},
 "Sofia Almeida": {"frequencia": 70, "exercicios": 50},
 "Bruno Teixeira": {"exercicios": 50},
 "Letícia Cardoso": {"exercicios": 50},
 "Gustavo Moreira": {"atrasos": 2, "exercicios": 50},
 "Daniel Azevedo": {"participacao": 4.5},
 "Caio Fernandes": {"participacao": 4.5, "exercicios": 50},
 "Carolina Ramos": {"atrasos": 2},
 "Natália Gomes": {"exercicios": 50},
 "Leonardo Pires": {"exercicios": 50},
 "Yasmin Correia": {"frequencia": 90, "prova": 7.8},
 "Miguel Araújo": {"atrasos": 2},
 "Helena Duarte": {"frequencia": 90},
 "Enzo Vieira": {"exercicios": 50},
 "Laura Campos": {"participacao": 4.5},
 "Samuel Cunha": {"frequencia": 70},
 "Lívia Neves": {"atrasos": 2, "exercicios": 50},
 "Cecília Tavares": {"exercicios": 50},
 "Nicolas Prado": {"participacao": 6.0},
 "Maitê Guimarães": {"frequencia": 70, "exercicios": 50},
 "Igor Batista": {"frequencia": 70},
 "Heloísa Rezende": {"atrasos": 0},
 "Otávio Coelho": {"exercicios": 50},
 "Wesley Braga": {"participacao": 4.5, "exercicios": 50},
 "Clara Pontes": {"atrasos": 2},
 "Melissa Xavier": {"atrasos": 2},
 "Vitor Hugo Dias": {"participacao": 4.5},
 "Sarah Paiva": {"frequencia": 90},
 "Heitor Fonseca": {"exercicios": 50},
 "Renan Leal": {"atrasos": 2},
 "João Pedro Matos": {"frequencia": 90},
 "Maria Eduarda Sales": {"participacao": 4.5},
 "Erick Cavalcante": {"exercicios": 70},
 "Brenda Rios": {"exercicios": 50},
 "Fernanda Lacerda": {"participacao": 4.5, "exercicios": 50},
 "Luiz Felipe Mota": {"atrasos": 0},
 "Tainá Soares": {"exercicios": 90},
 "Paulo César Dantas": {"participacao": 6.0}}

PADROES_DATAS = {
    1: [[0], [1], [2], [3]],
    2: [[0, 1], [0, 2], [0, 3], [1, 3], [2, 3]],
    3: [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]],
    4: [[0, 1, 2, 3]],
}


def indices_datas(quantidade: int, indice_aluno: int) -> list[int]:
    padroes = PADROES_DATAS[quantidade]
    return padroes[indice_aluno % len(padroes)]


def criar_registro_aluno(
    aluno_id: int,
    nome_aluno: str,
    perfil_nome: str,
    indice_data: int,
    indice_aluno: int,
    ultimo_indice_data: int,
) -> None:
    dados = PERFIS[perfil_nome][indice_data].copy()

    if indice_data == ultimo_indice_data:
        dados.update(
            AJUSTES_ULTIMO_REGISTRO.get(
                nome_aluno,
                {},
            )
        )

    aulas_dadas = 20 if indice_aluno % 2 == 0 else 40
    faltas = round(
        aulas_dadas * (1 - dados["frequencia"] / 100)
    )

    variacao = ((indice_aluno % 3) - 1) * 0.1
    perfis_sem_variacao = {
        "limiar_regular",
        "limiar_atencao",
        "limiar_prioridade",
    }

    nota_provas = dados["prova"]
    nota_atividades = dados["atividade"]
    participacao = dados["participacao"]

    if perfil_nome not in perfis_sem_variacao:
        nota_provas = min(10, max(0, nota_provas + variacao))
        nota_atividades = min(10, max(0, nota_atividades - variacao))
        participacao = min(10, max(0, participacao + variacao))

    taxa_exercicios = dados["exercicios"]
    if taxa_exercicios is None:
        exercicios_propostos = 0
        exercicios_resolvidos = 0
    else:
        exercicios_propostos = 20 if indice_aluno % 2 == 0 else 25
        exercicios_resolvidos = round(
            exercicios_propostos * taxa_exercicios / 100
        )

    atividades_entregues = max(
        2,
        8 - dados["atrasos"] + (indice_aluno % 2),
    )

    repo.criar_acompanhamento(
        Acompanhamento(
            aluno_id=aluno_id,
            data_registro=str(DATAS[indice_data]),
            aulas_dadas=aulas_dadas,
            faltas=faltas,
            nota_provas_obtida=round(nota_provas, 1),
            nota_provas_maxima=10,
            nota_atividades_obtida=round(nota_atividades, 1),
            nota_atividades_maxima=10,
            atividades_entregues=atividades_entregues,
            atividades_atrasadas=dados["atrasos"],
            participacao_aula=round(participacao, 1),
            exercicios_propostos=exercicios_propostos,
            exercicios_resolvidos=exercicios_resolvidos,
        )
    )


def seed_dados_demonstracao() -> None:
    if repo.listar_turmas():
        return

    for dados_turma in TURMAS:
        turma_id = repo.criar_turma(dados_turma["turma"])

        for indice, (nome, perfil, quantidade) in enumerate(
            dados_turma["alunos"]
        ):
            aluno_id = repo.criar_aluno(
                Aluno(
                    nome_aluno=nome,
                    matricula=str(
                        dados_turma["matricula_inicio"] + indice
                    ),
                    turma_id=turma_id,
                )
            )

            datas_aluno = indices_datas(
                quantidade,
                indice,
            )

            for indice_data in datas_aluno:
                criar_registro_aluno(
                    aluno_id,
                    nome,
                    perfil,
                    indice_data,
                    indice,
                    datas_aluno[-1],
                )
