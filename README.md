# 📊 DetectEdu

Aplicação web de **apoio à decisão pedagógica** que reúne indicadores acadêmicos em um dashboard para auxiliar professores no acompanhamento das turmas e na priorização de alunos que podem precisar de maior atenção.

O projeto utiliza dados fictícios para demonstração e uma classificação descritiva baseada em regras, sem finalidade diagnóstica.

---

## 📋 Sobre o Projeto

O **DetectEdu** centraliza informações que normalmente são analisadas separadamente, como frequência, notas, participação, atividades atrasadas, exercícios realizados e evolução do desempenho.

A partir desses indicadores, o sistema apresenta uma visão geral da turma e uma análise individual de cada aluno, facilitando a identificação de diferentes situações de acompanhamento pedagógico.

---

## ✨ Funcionalidades

- Cadastro, edição e exclusão de turmas e alunos.
- Registro periódico de acompanhamentos.
- Dashboard com indicadores gerais da turma.
- Distribuição dos alunos por classificação pedagógica.
- Comparação entre frequência e desempenho.
- Visualização das médias dos principais indicadores.
- Análise individual com perfil dos indicadores.
- Histórico de evolução do desempenho.
- Identificação de fatores de atenção.
- Sugestões de acompanhamento.
- Persistência local dos dados com SQLite.
- Base fictícia para demonstração do MVP.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Utilização |
| :--- | :--- |
| **Python** | Lógica da aplicação e processamento dos indicadores. |
| **Streamlit** | Interface web e dashboard. |
| **Pandas** | Organização e análise dos dados. |
| **Plotly** | Gráficos e visualizações interativas. |
| **SQLite** | Persistência local dos dados. |
| **CSS3** | Personalização visual da interface. |

---

## 📊 Classificação Pedagógica

A classificação é calculada a partir da combinação dos indicadores registrados para cada aluno.

| Pontuação | Classificação |
| :---: | :--- |
| **0 a 3** | Acompanhamento regular |
| **4 a 7** | Sinais de atenção |
| **8 ou mais** | Prioridade de acompanhamento |

São considerados frequência, notas de provas e atividades, atividades atrasadas, participação em aula, taxa de exercícios e evolução das notas.

Quando nenhum exercício foi proposto no período, esse indicador é tratado como **não aplicável** e não acrescenta pontos.

> A classificação é uma regra descritiva do MVP e funciona como apoio à priorização. Ela não representa diagnóstico e não substitui a avaliação do professor.

---

## 🧪 Dados de Demonstração

A base fictícia utilizada no protótipo possui:

- **3 turmas**
- **74 alunos**
- **196 registros de acompanhamento**
- Entre **1 e 4 acompanhamentos por aluno**

Os dados representam diferentes trajetórias, incluindo melhora, queda de desempenho, baixa frequência, dificuldades em notas, baixa participação, atrasos e situações próximas aos limites de classificação.

Os registros são determinísticos para que os mesmos cenários sejam reproduzidos durante testes e demonstrações.

---

## 📁 Estrutura do Projeto

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

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/mayasrl/DetectEdu.git
cd DetectEdu
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python -m streamlit run app.py
```

A aplicação estará disponível em:

```text
http://localhost:8501
```

Para preencher o sistema com a base fictícia, utilize o botão **Carregar dados de demonstração** na barra lateral.

---

<img width="1370" height="871" alt="Captura de tela 2026-08-17 114527" src="https://github.com/user-attachments/assets/554fd6ac-8601-4ece-85ca-27ff9bd5f943" />


---

<p align="center">
  Desenvolvido como projeto acadêmico em <strong>Ciência de Dados e Data Analytics</strong>, com 💛 por <strong>@mayasrl</strong>.
</p>
