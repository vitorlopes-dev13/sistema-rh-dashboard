import streamlit as st
import pandas as pd
import plotly.express as px
from database import criar_tabela
from operacoes import (
    cadastrar_funcionario,
    listar_funcionarios,
    deletar_funcionario,
    atualizar_funcionario
)

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Sistema RH", layout="wide", page_icon="👤")
criar_tabela()

# -------------------------
# HEADER
# -------------------------
st.markdown("<h1 style='text-align: center;'>🚀 Dashboard RH Profissional</h1>", unsafe_allow_html=True)
st.divider()

# -------------------------
# MENU 
# -------------------------
menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Cadastrar", "Funcionários"]
)

# -------------------------
# FUNÇÕES
# -------------------------
def carregar():
    dados = listar_funcionarios()
    if not dados:
        return pd.DataFrame(columns=["ID", "Nome", "Salário", "Situação"])
    
    return pd.DataFrame(
        [(f.id, f.nome, f.salario, f.situacao()) for f in dados],
        columns=["ID", "Nome", "Salário", "Situação"]
    )

# -------------------------
# DASHBOARD
# -------------------------
if menu == "Dashboard":
    df = carregar()

    if not df.empty:
        # FILTRO
        min_sal, max_sal = st.slider("Filtrar salário", 0, 10000, (0, 10000))
        df = df[(df["Salário"] >= min_sal) & (df["Salário"] <= max_sal)]

        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Funcionários", len(df))
        col2.metric("Média", f"R$ {df['Salário'].mean():,.2f}")
        col3.metric("Máximo", f"R$ {df['Salário'].max():,.2f}")
        col4.metric("Folha Total", f"R$ {df['Salário'].sum():,.2f}")

        st.divider()

        # GRÁFICOS
        st.subheader("📊 Salários por Funcionário")
        st.plotly_chart(px.bar(df, x="Nome", y="Salário", color="Salário"), use_container_width=True)

        st.subheader("📈 Distribuição Salarial")
        st.plotly_chart(px.histogram(df, x="Salário", nbins=10), use_container_width=True)

        # PIZZA
        def faixa(s):
            if s <= 2000:
                return "Até 2k"
            elif s <= 5000:
                return "2k-5k"
            return "5k+"

        df["Faixa"] = df["Salário"].apply(faixa)

        st.subheader("🥧 Faixa Salarial")
        st.plotly_chart(px.pie(df, names="Faixa"), use_container_width=True)

        # OUTLIERS
        q1 = df["Salário"].quantile(0.25)
        q3 = df["Salário"].quantile(0.75)
        iqr = q3 - q1

        outliers = df[
            (df["Salário"] < q1 - 1.5 * iqr) |
            (df["Salário"] > q3 + 1.5 * iqr)
        ]

        if not outliers.empty:
            st.warning("⚠️ Outliers detectados")
            st.dataframe(outliers)

    else:
        st.warning("Sem funcionários cadastrados")

# -------------------------
# CADASTRAR
# -------------------------
elif menu == "Cadastrar":
    st.subheader("➕ Cadastrar Funcionário")

    with st.form("form_cadastro", clear_on_submit=True):
        nome = st.text_input("Nome")
        salario = st.number_input("Salário", min_value=0.0)

        if st.form_submit_button("Cadastrar"):
            if not nome.strip():
                st.error("Nome é obrigatório")
            elif salario <= 0:
                st.warning("Salário deve ser maior que zero")
            else:
                cadastrar_funcionario(nome, salario)
                st.success("Funcionário cadastrado!")
                st.rerun()

# -------------------------
# FUNCIONÁRIOS
# -------------------------
elif menu == "Funcionários":
    st.subheader("📋 Lista de Funcionários")

    df = carregar()

    if not df.empty:
        busca = st.text_input("🔎 Buscar por nome")

        if busca:
            df = df[df["Nome"].str.contains(busca, case=False)]

        for _, row in df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([3,2,2,1,1])

            col1.write(row["Nome"])
            col2.write(f"R$ {row['Salário']:,.2f}")
            col3.write(row["Situação"])

            # EDITAR
            if col4.button("✏️", key=f"edit_{row['ID']}"):
                st.session_state["edit_id"] = row["ID"]

            # DELETAR
            if col5.button("❌", key=f"del_{row['ID']}"):
                deletar_funcionario(row["ID"])
                st.rerun()

        # FORM EDITAR
        if "edit_id" in st.session_state:
            st.divider()
            st.subheader("✏️ Editar Funcionário")

            funcionario = df[df["ID"] == st.session_state["edit_id"]].iloc[0]

            novo_nome = st.text_input("Novo Nome", value=funcionario["Nome"])
            novo_salario = st.number_input("Novo Salário", value=float(funcionario["Salário"]))

            if st.button("Salvar Alterações"):
                atualizar_funcionario(
                    st.session_state["edit_id"],
                    novo_nome,
                    novo_salario
                )
                del st.session_state["edit_id"]
                st.success("Atualizado com sucesso!")
                st.rerun()

        # BOTÃO CSV 
        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            "📥 Baixar CSV",
            data=csv,
            file_name="funcionarios.csv",
            mime="text/csv"
        )

    else:
        st.warning("Sem funcionários cadastrados")