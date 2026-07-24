from dataclasses import dataclass


@dataclass
class Turma:
    nome_turma: str
    curso: str
    disciplina: str
    semestre: str
    professor: str
    id: int | None = None

    def __str__(self) -> str:
        return f"{self.nome_turma} — {self.disciplina} ({self.semestre})"


@dataclass
class Aluno:
    nome_aluno: str
    matricula: str
    turma_id: int
    id: int | None = None

    def __str__(self) -> str:
        return f"{self.nome_aluno} ({self.matricula})"


@dataclass
class Acompanhamento:
    aluno_id: int
    data_registro: str
    aulas_dadas: int
    faltas: int
    nota_provas_obtida: float
    nota_provas_maxima: float
    nota_atividades_obtida: float
    nota_atividades_maxima: float
    atividades_entregues: int
    atividades_atrasadas: int
    participacao_aula: float
    exercicios_propostos: int
    exercicios_resolvidos: int
    id: int | None = None


CLASSIFICACAO_LABELS = {
    "sem_indicios": "Sem indícios de dificuldade",
    "atencao": "Atenção pedagógica",
    "intervencao": "Necessita intervenção",
}

CLASSIFICACAO_CORES = {
    "sem_indicios": "#2E7D32",
    "atencao": "#F57C00",
    "intervencao": "#C62828",
}
