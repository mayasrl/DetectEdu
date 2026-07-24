# DetectEdu

O **DetectEdu** é uma aplicação de apoio à decisão pedagógica desenvolvida como projeto da pós-graduação em Ciência de Dados.

O sistema organiza informações como frequência, notas, participação, atividades e exercícios, apresentando os resultados em um dashboard para auxiliar professores no acompanhamento das turmas e na identificação de alunos que podem precisar de atenção adicional.

O projeto está em fase de MVP e utiliza dados simulados para demonstração. A classificação atual é baseada em regras definidas para esta primeira versão e ainda será revisada e validada antes da publicação definitiva.

---

## Visão Geral

- **Python**: linguagem principal da aplicação.
- **Streamlit**: construção da interface web.
- **SQLite**: armazenamento local das informações.
- **Pandas**: organização e análise dos dados.
- **Plotly**: criação dos gráficos interativos.

---

## Funcionalidades

- Cadastro e edição de turmas.
- Cadastro e edição de alunos.
- Registro periódico de acompanhamentos.
- Armazenamento dos dados em SQLite.
- Dashboard com indicadores gerais da turma.
- Análise individual dos alunos.
- Visualização da evolução do desempenho.
- Classificação pedagógica descritiva.
- Identificação de fatores de atenção.
- Sugestões iniciais de acompanhamento.
- Dados simulados para demonstração.

---

## Estrutura do Projeto

```text
DetectEdu/
├── app.py
├── analytics.py
├── charts.py
├── dashboard.py
├── database.py
├── forms.py
├── models.py
├── repository.py
├── seed.py
├── services.py
├── styles.css
├── requirements.txt
└── README.md
```

---

## Como Executar

Clone o repositório:

```bash
git clone https://github.com/mayasrl/DetectEdu.git
cd DetectEdu
```

Crie e ative o ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute a aplicação:

```bash
python -m streamlit run app.py
```

Acesse `http://localhost:8501` no navegador.

---

## Dados de Demonstração

Para testar o sistema, clique em **Carregar dados de demonstração** na barra lateral da aplicação.

Os nomes, matrículas e indicadores utilizados são fictícios.

---

## Classificação Pedagógica

| Pontuação | Classificação |
|---|---|
| 0 a 3 | Sem indícios de dificuldade |
| 4 a 7 | Atenção pedagógica |
| 8 ou mais | Necessita intervenção |

A classificação considera frequência, notas, atividades atrasadas, participação, exercícios resolvidos e evolução do desempenho.

> A classificação atual é uma regra descritiva do MVP. Ela não representa diagnóstico e não substitui a avaliação do professor.

---

<p align="center">
  Desenvolvido como projeto da pós-graduação em <strong>Ciência de Dados</strong>, com 💛 por <strong>@mayasrl</strong>.
</p>