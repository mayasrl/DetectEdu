from pathlib import Path

import streamlit as st

import dashboard
import forms
import repository as repo
from database import initialize_database
from seed import seed_dados_demonstracao

st.set_page_config(
    page_title="DetectEdu",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def carregar_estilos() -> None:
    arquivo_css = Path(__file__).parent / "styles.css"
    estilos = arquivo_css.read_text(
        encoding="utf-8"
    )
    st.markdown(
        f"<style>{estilos}</style>",
        unsafe_allow_html=True,
    )


@st.cache_resource
def inicializar_banco() -> None:
    initialize_database()


carregar_estilos()
inicializar_banco()

with st.sidebar:
    st.markdown(
        """
        <div style="padding:12px 0 24px 0;">
            <div style="
                font-size:20px;
                font-weight:700;
                color:#E8EAF0;
            ">
                DetectEdu
            </div>
            <div style="
                font-size:12px;
                color:#636878;
                margin-top:4px;
            ">
                Apoio à decisão pedagógica
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pagina = st.radio(
        "Navegação",
        [
            "Dashboard",
            "Acompanhamentos",
            "Alunos",
            "Turmas",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    if st.button(
        "Carregar dados de demonstração",
        use_container_width=True,
    ):
        if repo.listar_turmas():
            st.info(
                "Já existem dados cadastrados no banco."
            )
        else:
            seed_dados_demonstracao()
            st.success(
                "Dados de demonstração carregados."
            )
            st.rerun()

    st.caption("DetectEdu · MVP")

if pagina == "Dashboard":
    dashboard.pagina_dashboard()
elif pagina == "Acompanhamentos":
    forms.pagina_acompanhamento()
elif pagina == "Alunos":
    forms.pagina_alunos()
else:
    forms.pagina_turmas()
