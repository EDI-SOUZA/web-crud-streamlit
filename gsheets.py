import gspread
import json
import os
from google.oauth2.service_account import Credentials
import streamlit as st  # necessário para mostrar erros no Streamlit

def get_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    if 'GOOGLE_SHEETS_CREDENTIALS_JSON' in os.environ:
        creds_dict = json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON"))
    else:
        with open('credentials.json') as f:
            creds_dict = json.load(f)
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    return gspread.authorize(creds)

def get_sheet():
    try:
        client = get_client()
        sheet = client.open("Consultas Agendadas").sheet1
        if not sheet.row_values(1):
            sheet.append_row(["nome", "data_ nascimento", "cpf", "telefone", "email"])
        return sheet
    except Exception as e:
        st.error(f"Erro ao acessar a planilha: {e}")
        import traceback
        st.error(traceback.format_exc())
        return None


def add_dado(nome, data_nascimento, cpf, telefone, email):
    sheet = get_sheet()
    if sheet:
        dados = listar_dados()
        for dado in dados:
            if dado.get("nome") == nome and dado.get("data_nascimento") == data_nascimento and dado.get("cpf") == cpf and dado.get("telefone") == telefone and dado.get("email") == email:
                return False  # Já existe
        sheet.append_row([nome, data_nascimento, cpf, telefone, email])
        return True
    return False

def listar_dados():
    sheet = get_sheet()
    if sheet:
        try:
            return sheet.get_all_records()
        except Exception:
            return []
    return []