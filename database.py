import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "detectedu.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS turmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_turma TEXT NOT NULL,
                curso TEXT NOT NULL,
                disciplina TEXT NOT NULL,
                semestre TEXT NOT NULL,
                professor TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_aluno TEXT NOT NULL,
                matricula TEXT NOT NULL UNIQUE,
                turma_id INTEGER NOT NULL,
                FOREIGN KEY (turma_id)
                    REFERENCES turmas(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS acompanhamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                data_registro TEXT NOT NULL,
                aulas_dadas INTEGER NOT NULL DEFAULT 0,
                faltas INTEGER NOT NULL DEFAULT 0,
                nota_provas_obtida REAL NOT NULL DEFAULT 0,
                nota_provas_maxima REAL NOT NULL DEFAULT 10,
                nota_atividades_obtida REAL NOT NULL DEFAULT 0,
                nota_atividades_maxima REAL NOT NULL DEFAULT 10,
                atividades_entregues INTEGER NOT NULL DEFAULT 0,
                atividades_atrasadas INTEGER NOT NULL DEFAULT 0,
                participacao_aula REAL NOT NULL DEFAULT 0,
                exercicios_propostos INTEGER NOT NULL DEFAULT 0,
                exercicios_resolvidos INTEGER NOT NULL DEFAULT 0,
                UNIQUE (aluno_id, data_registro),
                FOREIGN KEY (aluno_id)
                    REFERENCES alunos(id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_alunos_turma
            ON alunos(turma_id);

            CREATE INDEX IF NOT EXISTS idx_acompanhamentos_aluno
            ON acompanhamentos(aluno_id);
            """
        )
