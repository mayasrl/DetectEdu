import random
from datetime import date

import repository as repo
from models import Acompanhamento, Aluno, Turma


def seed_dados_demonstracao() -> None:
    if repo.listar_turmas():
        return

    random.seed(42)

    turma_ads = repo.criar_turma(
        Turma(
            nome_turma="ADS - Manhã",
            curso="Análise e Desenvolvimento de Sistemas",
            disciplina="Algoritmos e Programação",
            semestre="2025.1",
            professor="Carlos Menezes",
        )
    )
    turma_cc = repo.criar_turma(
        Turma(
            nome_turma="CC - Noite",
            curso="Ciência da Computação",
            disciplina="Estrutura de Dados",
            semestre="2025.1",
            professor="Ana Rodrigues",
        )
    )

    alunos_ads = [
        ("Lucas Ferreira", "20250101"),
        ("Mariana Souza", "20250102"),
        ("Felipe Alves", "20250103"),
        ("Beatriz Costa", "20250104"),
        ("Rafael Mendes", "20250105"),
        ("Amanda Oliveira", "20250106"),
        ("Thiago Santos", "20250107"),
        ("Larissa Pereira", "20250108"),
    ]
    alunos_cc = [
        ("João Victor Lima", "20250201"),
        ("Carolina Ramos", "20250202"),
        ("Eduardo Barros", "20250203"),
        ("Natália Gomes", "20250204"),
        ("Pedro Henrique Silva", "20250205"),
    ]

    perfis = {
        "bom": {
            "frequencia_minima": 88,
            "nota_minima": 7.5,
            "atrasos": 0,
            "participacao_minima": 7.5,
            "exercicios_minimos": 80,
        },
        "medio": {
            "frequencia_minima": 78,
            "nota_minima": 6.0,
            "atrasos": 2,
            "participacao_minima": 5.5,
            "exercicios_minimos": 65,
        },
        "critico": {
            "frequencia_minima": 60,
            "nota_minima": 4.0,
            "atrasos": 4,
            "participacao_minima": 3.5,
            "exercicios_minimos": 45,
        },
    }

    perfis_ads = [
        "bom",
        "bom",
        "bom",
        "medio",
        "medio",
        "medio",
        "critico",
        "critico",
    ]
    perfis_cc = [
        "bom",
        "bom",
        "medio",
        "medio",
        "critico",
    ]

    datas = [
        date(2025, 3, 15),
        date(2025, 4, 20),
        date(2025, 5, 25),
    ]

    def gerar_registros(
        aluno_id: int,
        nome_perfil: str,
    ) -> None:
        perfil = perfis[nome_perfil]

        for data_registro in datas:
            aulas = random.choice([24, 32, 40])
            frequencia = random.uniform(
                perfil["frequencia_minima"],
                min(
                    perfil["frequencia_minima"] + 12,
                    100,
                ),
            )
            faltas = round(
                aulas * (1 - frequencia / 100)
            )

            nota_provas = round(
                random.uniform(
                    perfil["nota_minima"],
                    min(
                        perfil["nota_minima"] + 2,
                        10,
                    ),
                ),
                1,
            )
            nota_atividades = round(
                random.uniform(
                    max(
                        perfil["nota_minima"] - 0.5,
                        0,
                    ),
                    min(
                        perfil["nota_minima"] + 1.5,
                        10,
                    ),
                ),
                1,
            )
            participacao = round(
                random.uniform(
                    perfil["participacao_minima"],
                    min(
                        perfil["participacao_minima"] + 2,
                        10,
                    ),
                ),
                1,
            )

            exercicios_propostos = random.choice(
                [15, 20, 25]
            )
            taxa_exercicios = random.uniform(
                perfil["exercicios_minimos"],
                min(
                    perfil["exercicios_minimos"] + 20,
                    100,
                ),
            )
            exercicios_resolvidos = round(
                exercicios_propostos
                * taxa_exercicios
                / 100
            )
            atividades_atrasadas = max(
                0,
                perfil["atrasos"]
                + random.randint(-1, 1),
            )

            repo.criar_acompanhamento(
                Acompanhamento(
                    aluno_id=aluno_id,
                    data_registro=str(data_registro),
                    aulas_dadas=aulas,
                    faltas=faltas,
                    nota_provas_obtida=nota_provas,
                    nota_provas_maxima=10,
                    nota_atividades_obtida=nota_atividades,
                    nota_atividades_maxima=10,
                    atividades_entregues=random.randint(
                        4,
                        8,
                    ),
                    atividades_atrasadas=atividades_atrasadas,
                    participacao_aula=participacao,
                    exercicios_propostos=exercicios_propostos,
                    exercicios_resolvidos=exercicios_resolvidos,
                )
            )

    for dados_aluno, perfil in zip(
        alunos_ads,
        perfis_ads,
    ):
        nome, matricula = dados_aluno
        aluno_id = repo.criar_aluno(
            Aluno(
                nome_aluno=nome,
                matricula=matricula,
                turma_id=turma_ads,
            )
        )
        gerar_registros(
            aluno_id,
            perfil,
        )

    for dados_aluno, perfil in zip(
        alunos_cc,
        perfis_cc,
    ):
        nome, matricula = dados_aluno
        aluno_id = repo.criar_aluno(
            Aluno(
                nome_aluno=nome,
                matricula=matricula,
                turma_id=turma_cc,
            )
        )
        gerar_registros(
            aluno_id,
            perfil,
        )
