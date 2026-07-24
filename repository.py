import sqlite3

from database import get_connection
from models import Acompanhamento, Aluno, Turma


def listar_turmas() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM turmas ORDER BY nome_turma"
        ).fetchall()


def buscar_turma(turma_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM turmas WHERE id = ?",
            (turma_id,),
        ).fetchone()


def criar_turma(turma: Turma) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO turmas (
                nome_turma,
                curso,
                disciplina,
                semestre,
                professor
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                turma.nome_turma,
                turma.curso,
                turma.disciplina,
                turma.semestre,
                turma.professor,
            ),
        )
        return cursor.lastrowid


def atualizar_turma(turma: Turma) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE turmas
            SET nome_turma = ?,
                curso = ?,
                disciplina = ?,
                semestre = ?,
                professor = ?
            WHERE id = ?
            """,
            (
                turma.nome_turma,
                turma.curso,
                turma.disciplina,
                turma.semestre,
                turma.professor,
                turma.id,
            ),
        )


def deletar_turma(turma_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM turmas WHERE id = ?",
            (turma_id,),
        )


def listar_alunos(turma_id: int | None = None) -> list[sqlite3.Row]:
    with get_connection() as conn:
        if turma_id is not None:
            return conn.execute(
                """
                SELECT *
                FROM alunos
                WHERE turma_id = ?
                ORDER BY nome_aluno
                """,
                (turma_id,),
            ).fetchall()

        return conn.execute(
            "SELECT * FROM alunos ORDER BY nome_aluno"
        ).fetchall()


def buscar_aluno(aluno_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM alunos WHERE id = ?",
            (aluno_id,),
        ).fetchone()


def matricula_existe(
    matricula: str,
    excluir_id: int | None = None,
) -> bool:
    with get_connection() as conn:
        if excluir_id is not None:
            row = conn.execute(
                """
                SELECT id
                FROM alunos
                WHERE matricula = ?
                  AND id != ?
                """,
                (matricula, excluir_id),
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT id FROM alunos WHERE matricula = ?",
                (matricula,),
            ).fetchone()

    return row is not None


def criar_aluno(aluno: Aluno) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO alunos (
                nome_aluno,
                matricula,
                turma_id
            )
            VALUES (?, ?, ?)
            """,
            (
                aluno.nome_aluno,
                aluno.matricula,
                aluno.turma_id,
            ),
        )
        return cursor.lastrowid


def atualizar_aluno(aluno: Aluno) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE alunos
            SET nome_aluno = ?,
                matricula = ?,
                turma_id = ?
            WHERE id = ?
            """,
            (
                aluno.nome_aluno,
                aluno.matricula,
                aluno.turma_id,
                aluno.id,
            ),
        )


def deletar_aluno(aluno_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM alunos WHERE id = ?",
            (aluno_id,),
        )


def listar_acompanhamentos(aluno_id: int) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT *
            FROM acompanhamentos
            WHERE aluno_id = ?
            ORDER BY data_registro
            """,
            (aluno_id,),
        ).fetchall()


def buscar_acompanhamento(
    acompanhamento_id: int,
) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT *
            FROM acompanhamentos
            WHERE id = ?
            """,
            (acompanhamento_id,),
        ).fetchone()


def acompanhamento_existe(
    aluno_id: int,
    data_registro: str,
    excluir_id: int | None = None,
) -> bool:
    query = """
        SELECT id
        FROM acompanhamentos
        WHERE aluno_id = ?
          AND data_registro = ?
    """
    parametros: list[object] = [aluno_id, data_registro]

    if excluir_id is not None:
        query += " AND id != ?"
        parametros.append(excluir_id)

    with get_connection() as conn:
        row = conn.execute(
            query,
            parametros,
        ).fetchone()

    return row is not None


def criar_acompanhamento(
    acompanhamento: Acompanhamento,
) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO acompanhamentos (
                aluno_id,
                data_registro,
                aulas_dadas,
                faltas,
                nota_provas_obtida,
                nota_provas_maxima,
                nota_atividades_obtida,
                nota_atividades_maxima,
                atividades_entregues,
                atividades_atrasadas,
                participacao_aula,
                exercicios_propostos,
                exercicios_resolvidos
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                acompanhamento.aluno_id,
                acompanhamento.data_registro,
                acompanhamento.aulas_dadas,
                acompanhamento.faltas,
                acompanhamento.nota_provas_obtida,
                acompanhamento.nota_provas_maxima,
                acompanhamento.nota_atividades_obtida,
                acompanhamento.nota_atividades_maxima,
                acompanhamento.atividades_entregues,
                acompanhamento.atividades_atrasadas,
                acompanhamento.participacao_aula,
                acompanhamento.exercicios_propostos,
                acompanhamento.exercicios_resolvidos,
            ),
        )
        return cursor.lastrowid


def atualizar_acompanhamento(
    acompanhamento: Acompanhamento,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE acompanhamentos
            SET data_registro = ?,
                aulas_dadas = ?,
                faltas = ?,
                nota_provas_obtida = ?,
                nota_provas_maxima = ?,
                nota_atividades_obtida = ?,
                nota_atividades_maxima = ?,
                atividades_entregues = ?,
                atividades_atrasadas = ?,
                participacao_aula = ?,
                exercicios_propostos = ?,
                exercicios_resolvidos = ?
            WHERE id = ?
            """,
            (
                acompanhamento.data_registro,
                acompanhamento.aulas_dadas,
                acompanhamento.faltas,
                acompanhamento.nota_provas_obtida,
                acompanhamento.nota_provas_maxima,
                acompanhamento.nota_atividades_obtida,
                acompanhamento.nota_atividades_maxima,
                acompanhamento.atividades_entregues,
                acompanhamento.atividades_atrasadas,
                acompanhamento.participacao_aula,
                acompanhamento.exercicios_propostos,
                acompanhamento.exercicios_resolvidos,
                acompanhamento.id,
            ),
        )


def deletar_acompanhamento(
    acompanhamento_id: int,
) -> None:
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM acompanhamentos WHERE id = ?",
            (acompanhamento_id,),
        )


def ultimo_acompanhamento(
    aluno_id: int,
) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT *
            FROM acompanhamentos
            WHERE aluno_id = ?
            ORDER BY data_registro DESC
            LIMIT 1
            """,
            (aluno_id,),
        ).fetchone()


def penultimo_acompanhamento(
    aluno_id: int,
) -> sqlite3.Row | None:
    with get_connection() as conn:
        registros = conn.execute(
            """
            SELECT *
            FROM acompanhamentos
            WHERE aluno_id = ?
            ORDER BY data_registro DESC
            LIMIT 2
            """,
            (aluno_id,),
        ).fetchall()

    if len(registros) < 2:
        return None

    return registros[1]
