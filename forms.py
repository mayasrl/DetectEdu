from datetime import date

import streamlit as st

import repository as repo
from models import Acompanhamento, Aluno, Turma


def _exibir_erros(erros: list[str]) -> None:
    for erro in erros:
        st.error(erro)


def _form_turma(
    dados_iniciais: dict | None = None,
) -> dict | None:
    dados = dados_iniciais or {}

    with st.form(
        "form_turma",
        clear_on_submit=False,
    ):
        nome = st.text_input(
            "Nome da turma",
            value=dados.get("nome_turma", ""),
        )
        curso = st.text_input(
            "Curso",
            value=dados.get("curso", ""),
        )
        disciplina = st.text_input(
            "Disciplina",
            value=dados.get("disciplina", ""),
        )
        semestre = st.text_input(
            "Semestre",
            value=dados.get("semestre", ""),
        )
        professor = st.text_input(
            "Professor",
            value=dados.get("professor", ""),
        )
        enviado = st.form_submit_button("Salvar")

    if not enviado:
        return None

    erros: list[str] = []

    if not nome.strip():
        erros.append(
            "O nome da turma é obrigatório."
        )
    if not curso.strip():
        erros.append("O curso é obrigatório.")
    if not disciplina.strip():
        erros.append(
            "A disciplina é obrigatória."
        )
    if not semestre.strip():
        erros.append("O semestre é obrigatório.")
    if not professor.strip():
        erros.append(
            "O nome do professor é obrigatório."
        )

    if erros:
        _exibir_erros(erros)
        return None

    return {
        "nome_turma": nome.strip(),
        "curso": curso.strip(),
        "disciplina": disciplina.strip(),
        "semestre": semestre.strip(),
        "professor": professor.strip(),
    }


def pagina_turmas() -> None:
    st.header("Turmas")

    turmas = repo.listar_turmas()
    modo = st.radio(
        "Ação",
        [
            "Cadastrar nova turma",
            "Editar turma existente",
        ],
        horizontal=True,
    )

    if modo == "Cadastrar nova turma":
        st.subheader("Nova turma")
        dados = _form_turma()

        if dados is not None:
            repo.criar_turma(Turma(**dados))
            st.success(
                "Turma cadastrada com sucesso."
            )
            st.rerun()

    else:
        if not turmas:
            st.info("Nenhuma turma cadastrada.")
            return

        opcoes = {
            (
                f"{turma['nome_turma']} — "
                f"{turma['disciplina']} "
                f"({turma['semestre']})"
            ): turma["id"]
            for turma in turmas
        }
        selecionada = st.selectbox(
            "Selecione a turma",
            list(opcoes),
        )
        turma_id = opcoes[selecionada]
        turma = repo.buscar_turma(turma_id)

        if turma is None:
            st.error("Turma não encontrada.")
            return

        st.subheader("Editar turma")
        dados = _form_turma(
            dados_iniciais=dict(turma)
        )

        if dados is not None:
            repo.atualizar_turma(
                Turma(
                    **dados,
                    id=turma_id,
                )
            )
            st.success("Turma atualizada.")
            st.rerun()

        st.divider()

        with st.expander(
            "Excluir turma",
            expanded=False,
        ):
            st.warning(
                "A turma, os alunos e os acompanhamentos "
                "vinculados serão removidos."
            )
            if st.button(
                "Confirmar exclusão",
                key="excluir_turma",
            ):
                repo.deletar_turma(turma_id)
                st.success("Turma removida.")
                st.rerun()

    turmas = repo.listar_turmas()

    if turmas:
        st.divider()
        st.subheader("Turmas cadastradas")

        for turma in turmas:
            st.markdown(
                f"**{turma['nome_turma']}** · "
                f"{turma['disciplina']} · "
                f"{turma['semestre']} · "
                f"{turma['professor']}"
            )


def pagina_alunos() -> None:
    st.header("Alunos")

    turmas = repo.listar_turmas()
    if not turmas:
        st.info(
            "Cadastre uma turma antes de adicionar alunos."
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
    modo = st.radio(
        "Ação",
        [
            "Cadastrar novo aluno",
            "Editar aluno existente",
        ],
        horizontal=True,
    )

    if modo == "Cadastrar novo aluno":
        st.subheader("Novo aluno")

        with st.form("form_aluno_novo"):
            turma_selecionada = st.selectbox(
                "Turma",
                list(opcoes_turma),
            )
            nome = st.text_input("Nome completo")
            matricula = st.text_input("Matrícula")
            enviado = st.form_submit_button("Salvar")

        if enviado:
            erros: list[str] = []

            if not nome.strip():
                erros.append(
                    "O nome do aluno é obrigatório."
                )

            if not matricula.strip():
                erros.append(
                    "A matrícula é obrigatória."
                )
            elif repo.matricula_existe(
                matricula.strip()
            ):
                erros.append(
                    "A matrícula já está cadastrada."
                )

            if erros:
                _exibir_erros(erros)
                return

            repo.criar_aluno(
                Aluno(
                    nome_aluno=nome.strip(),
                    matricula=matricula.strip(),
                    turma_id=opcoes_turma[
                        turma_selecionada
                    ],
                )
            )
            st.success(
                "Aluno cadastrado com sucesso."
            )
            st.rerun()

    else:
        turma_selecionada = st.selectbox(
            "Filtrar por turma",
            list(opcoes_turma),
            key="turma_alunos",
        )
        turma_id = opcoes_turma[turma_selecionada]
        alunos = repo.listar_alunos(turma_id)

        if not alunos:
            st.info(
                "Nenhum aluno cadastrado nesta turma."
            )
            return

        opcoes_aluno = {
            (
                f"{aluno['nome_aluno']} "
                f"({aluno['matricula']})"
            ): aluno["id"]
            for aluno in alunos
        }
        aluno_selecionado = st.selectbox(
            "Aluno",
            list(opcoes_aluno),
        )
        aluno_id = opcoes_aluno[
            aluno_selecionado
        ]
        aluno = repo.buscar_aluno(aluno_id)

        if aluno is None:
            st.error("Aluno não encontrado.")
            return

        st.subheader("Editar aluno")

        with st.form("form_aluno_editar"):
            nomes_turmas = list(opcoes_turma)
            turma_atual = next(
                (
                    nome
                    for nome, id_turma
                    in opcoes_turma.items()
                    if id_turma == aluno["turma_id"]
                ),
                nomes_turmas[0],
            )
            nova_turma = st.selectbox(
                "Turma",
                nomes_turmas,
                index=nomes_turmas.index(
                    turma_atual
                ),
            )
            nome = st.text_input(
                "Nome completo",
                value=aluno["nome_aluno"],
            )
            matricula = st.text_input(
                "Matrícula",
                value=aluno["matricula"],
            )
            enviado = st.form_submit_button("Salvar")

        if enviado:
            erros: list[str] = []

            if not nome.strip():
                erros.append(
                    "O nome do aluno é obrigatório."
                )

            if not matricula.strip():
                erros.append(
                    "A matrícula é obrigatória."
                )
            elif repo.matricula_existe(
                matricula.strip(),
                excluir_id=aluno_id,
            ):
                erros.append(
                    "A matrícula já pertence a outro aluno."
                )

            if erros:
                _exibir_erros(erros)
                return

            repo.atualizar_aluno(
                Aluno(
                    nome_aluno=nome.strip(),
                    matricula=matricula.strip(),
                    turma_id=opcoes_turma[
                        nova_turma
                    ],
                    id=aluno_id,
                )
            )
            st.success("Aluno atualizado.")
            st.rerun()

        st.divider()

        with st.expander(
            "Excluir aluno",
            expanded=False,
        ):
            st.warning(
                "O aluno e todos os acompanhamentos "
                "vinculados serão removidos."
            )
            if st.button(
                "Confirmar exclusão",
                key="excluir_aluno",
            ):
                repo.deletar_aluno(aluno_id)
                st.success("Aluno removido.")
                st.rerun()


def pagina_acompanhamento() -> None:
    st.header("Acompanhamentos")

    turmas = repo.listar_turmas()
    if not turmas:
        st.info("Nenhuma turma cadastrada.")
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
    )
    turma_id = opcoes_turma[turma_selecionada]

    alunos = repo.listar_alunos(turma_id)
    if not alunos:
        st.info(
            "Nenhum aluno cadastrado nesta turma."
        )
        return

    opcoes_aluno = {
        (
            f"{aluno['nome_aluno']} "
            f"({aluno['matricula']})"
        ): aluno["id"]
        for aluno in alunos
    }
    aluno_selecionado = st.selectbox(
        "Aluno",
        list(opcoes_aluno),
    )
    aluno_id = opcoes_aluno[aluno_selecionado]

    acompanhamentos = repo.listar_acompanhamentos(
        aluno_id
    )
    modo = st.radio(
        "Ação",
        [
            "Novo registro",
            "Editar registro existente",
        ],
        horizontal=True,
    )

    if modo == "Novo registro":
        _form_acompanhamento(aluno_id)
        return

    if not acompanhamentos:
        st.info(
            "Nenhum acompanhamento registrado para este aluno."
        )
        return

    opcoes_registro = {
        acompanhamento["data_registro"]: acompanhamento[
            "id"
        ]
        for acompanhamento in reversed(
            acompanhamentos
        )
    }
    registro_selecionado = st.selectbox(
        "Registro",
        list(opcoes_registro),
    )
    registro_id = opcoes_registro[
        registro_selecionado
    ]
    registro = repo.buscar_acompanhamento(
        registro_id
    )

    if registro is None:
        st.error("Registro não encontrado.")
        return

    _form_acompanhamento(
        aluno_id,
        dados_iniciais=dict(registro),
    )

    st.divider()

    with st.expander(
        "Excluir registro",
        expanded=False,
    ):
        if st.button(
            "Confirmar exclusão",
            key="excluir_registro",
        ):
            repo.deletar_acompanhamento(
                registro_id
            )
            st.success("Registro removido.")
            st.rerun()


def _form_acompanhamento(
    aluno_id: int,
    dados_iniciais: dict | None = None,
) -> None:
    dados = dados_iniciais or {}
    editando = dados_iniciais is not None
    chave_formulario = (
        "form_acompanhamento_editar"
        if editando
        else "form_acompanhamento_novo"
    )

    with st.form(chave_formulario):
        coluna_esquerda, coluna_direita = (
            st.columns(2)
        )

        with coluna_esquerda:
            data_registro = st.date_input(
                "Data do registro",
                value=(
                    date.fromisoformat(
                        dados["data_registro"]
                    )
                    if dados.get("data_registro")
                    else date.today()
                ),
            )
            aulas_dadas = st.number_input(
                "Aulas dadas",
                min_value=0,
                value=int(
                    dados.get("aulas_dadas", 0)
                ),
            )
            faltas = st.number_input(
                "Faltas",
                min_value=0,
                value=int(
                    dados.get("faltas", 0)
                ),
            )
            participacao = st.number_input(
                "Participação em aula (0–10)",
                min_value=0.0,
                max_value=10.0,
                step=0.5,
                value=float(
                    dados.get(
                        "participacao_aula",
                        5.0,
                    )
                ),
            )

        with coluna_direita:
            nota_provas_obtida = st.number_input(
                "Nota de provas obtida",
                min_value=0.0,
                value=float(
                    dados.get(
                        "nota_provas_obtida",
                        0.0,
                    )
                ),
            )
            nota_provas_maxima = st.number_input(
                "Nota máxima das provas",
                min_value=0.1,
                value=float(
                    dados.get(
                        "nota_provas_maxima",
                        10.0,
                    )
                ),
            )
            nota_atividades_obtida = st.number_input(
                "Nota de atividades obtida",
                min_value=0.0,
                value=float(
                    dados.get(
                        "nota_atividades_obtida",
                        0.0,
                    )
                ),
            )
            nota_atividades_maxima = st.number_input(
                "Nota máxima das atividades",
                min_value=0.1,
                value=float(
                    dados.get(
                        "nota_atividades_maxima",
                        10.0,
                    )
                ),
            )

        coluna_atividades, coluna_exercicios = (
            st.columns(2)
        )

        with coluna_atividades:
            atividades_entregues = st.number_input(
                "Atividades entregues",
                min_value=0,
                value=int(
                    dados.get(
                        "atividades_entregues",
                        0,
                    )
                ),
            )
            atividades_atrasadas = st.number_input(
                "Atividades atrasadas",
                min_value=0,
                value=int(
                    dados.get(
                        "atividades_atrasadas",
                        0,
                    )
                ),
            )

        with coluna_exercicios:
            exercicios_propostos = st.number_input(
                "Exercícios propostos",
                min_value=0,
                value=int(
                    dados.get(
                        "exercicios_propostos",
                        0,
                    )
                ),
            )
            exercicios_resolvidos = st.number_input(
                "Exercícios resolvidos",
                min_value=0,
                value=int(
                    dados.get(
                        "exercicios_resolvidos",
                        0,
                    )
                ),
            )

        enviado = st.form_submit_button(
            "Salvar registro"
        )

    if not enviado:
        return

    erros: list[str] = []

    if aulas_dadas == 0:
        erros.append(
            "Informe ao menos uma aula dada."
        )

    if faltas > aulas_dadas:
        erros.append(
            "O número de faltas não pode ser maior "
            "que o número de aulas dadas."
        )

    if nota_provas_obtida > nota_provas_maxima:
        erros.append(
            "A nota de provas obtida não pode ser "
            "maior que a nota máxima."
        )

    if (
        nota_atividades_obtida
        > nota_atividades_maxima
    ):
        erros.append(
            "A nota de atividades obtida não pode "
            "ser maior que a nota máxima."
        )

    if exercicios_resolvidos > exercicios_propostos:
        erros.append(
            "A quantidade de exercícios resolvidos "
            "não pode ser maior que a quantidade proposta."
        )

    data_texto = str(data_registro)

    if repo.acompanhamento_existe(
        aluno_id,
        data_texto,
        excluir_id=dados.get("id"),
    ):
        erros.append(
            "Já existe um registro para este aluno nesta data."
        )

    if erros:
        _exibir_erros(erros)
        return

    acompanhamento = Acompanhamento(
        aluno_id=aluno_id,
        data_registro=data_texto,
        aulas_dadas=aulas_dadas,
        faltas=faltas,
        nota_provas_obtida=nota_provas_obtida,
        nota_provas_maxima=nota_provas_maxima,
        nota_atividades_obtida=nota_atividades_obtida,
        nota_atividades_maxima=nota_atividades_maxima,
        atividades_entregues=atividades_entregues,
        atividades_atrasadas=atividades_atrasadas,
        participacao_aula=participacao,
        exercicios_propostos=exercicios_propostos,
        exercicios_resolvidos=exercicios_resolvidos,
        id=dados.get("id"),
    )

    if editando:
        repo.atualizar_acompanhamento(
            acompanhamento
        )
        st.success("Registro atualizado.")
    else:
        repo.criar_acompanhamento(
            acompanhamento
        )
        st.success("Registro salvo.")

    st.rerun()
