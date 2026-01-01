import streamlit as st
import pandas as pd

# URL da sua planilha
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1JiQypuz5pqfDgEmWbv2e808oXvcaxPUE/export?format=csv"

st.set_page_config(layout="wide", page_title="PSMCOL SISTEMA")

# Sistema de Login
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align:center;'>🔒 ACESSO PSMCOL</h2>", unsafe_allow_html=True)
    u = st.text_input("USUÁRIO").upper().strip()
    s = st.text_input("SENHA", type="password").strip()
    if st.button("ENTRAR NO SISTEMA"):
        if u == "ADMINISTRADOR" and s == "123321":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Dados incorretos")
    st.stop()

# Interface Principal
st.title("📊 Consulta de Internos")

try:
    df = pd.read_csv(URL_PLANILHA)
    busca = st.text_input("🔍 Digite o Nome ou Inforpen para buscar").upper()
    
    if busca:
        df_filtrado = df[df.astype(str).apply(lambda x: busca.lower() in x.str.lower().values, axis=1)]
    else:
        df_filtrado = df

    if df_filtrado.empty:
        st.warning("Nenhum registro encontrado.")
    else:
        st.write(f"Encontrados {len(df_filtrado)} registros.")
        st.dataframe(df_filtrado, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao conectar com a planilha: {e}")
