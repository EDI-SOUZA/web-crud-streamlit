import streamlit as st
from gsheets import add_dado, listar_dados

st.set_page_config(page_title="Agenda", layout="centered")
st.title("Agenda de Consultas")

with st.form("form_contato"):
    nome = st.text_input("Nome")
    data_nascimento = st.text_input("Data de Nascimento")
    cpf = st.text_input("Cpf")
    telefone = st.text_input("Telefone")
    email = st.text_input("Email")
    enviar = st.form_submit_button("Salvar")

    if enviar:
        if nome and email:
            sucesso = add_dado(nome, data_nascimento, cpf, telefone, email)
            if sucesso:
                st.success("Contato salvo com sucesso!")
            else:
                st.warning("Contato já existe na lista.")
        else:
            st.warning("Preencha todos os campos.")

st.subheader("📋 Dados cadastrados")
dados = listar_dados()

if dados:
    for d in dados:
        st.write(f"**{d.get('nome', '')}** - {d.get('data_nascimento', '')} - {d.get('cpf', '')} - {d.get('telefone', '')} - {d.get('email', '')}")
else:
    st.info("Nenhum dado cadastrado.")