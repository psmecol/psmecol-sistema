import streamlit as st
import pandas as pd

# --- MUITO IMPORTANTE: COLE O LINK DA SUA PLANILHA GOOGLE ABAIXO ---
# O link deve terminar exatamente em /export?format=csv
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1JiQypuz5pqfDgEmWbv2e808oXvcaxPUE/export?format=csv"
st.set_page_config(layout="wide", page_title="SISTEMA PSMECOL")

# Sistema de Login
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>🛡️ LOGIN - PSMECOL</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        u = st.text_input("USUÁRIO").upper().strip()
        s = st.text_input("SENHA", type="password").strip()
        if st.button("ENTRAR NO SISTEMA"):
            if u == "TARCIZIO" and s == "123321":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# Carregamento de Dados
@st.cache_data(ttl=60)
def carregar_dados():
    try:
        return pd.read_csv(URL_PLANILHA).fillna("-")
    except:
        return None

df = carregar_dados()

if df is not None:
    st.sidebar.title("MENU")
    setor = st.sidebar.selectbox("ESCOLHA O SETOR", ["STATUS", "ESCOLA", "SEGURANÇA", "LAVANDERIA"])
    
    # Exemplo Setor Escola (Mostrando as colunas que você pediu)
    if setor == "ESCOLA":
        st.header("👨‍🏫 SETOR ESCOLA")
        # Mostra colunas básicas + colunas 14 a 20
        st.dataframe(df.iloc[:, [0,1,3,14,15,16,17,18,19,20]], use_container_width=True, hide_index=True)
else:
    st.error("⚠️ Erro ao carregar a planilha. Verifique se o link no código está correto e se ela foi partilhada para 'Qualquer pessoa com o link'.")
