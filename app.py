import os, time, subprocess
import pandas as pd

# --- 1. PREPARAÇÃO DO AMBIENTE ---
# Remove processos antigos para não dar erro
!pkill -9 cloudflared
!pkill -9 streamlit
# Instala apenas o necessário (pandas, streamlit e leitor de excel)
!pip install -q streamlit pandas openpyxl

# --- 2. CONFIGURAÇÃO DO ACESSO EXTERNO (TÚNEL) ---
# Baixa o Cloudflared para gerar o link que pula o bloqueio da sua rede
if not os.path.exists("cloudflared"):
    !wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
    !chmod +x cloudflared

# --- 3. CRIAÇÃO DO ARQUIVO DO SISTEMA (app.py) ---
with open('app.py', 'w', encoding='utf-8') as f:
    f.write('''
import streamlit as st
import pandas as pd

# URL da sua planilha configurada para exportar como CSV
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
    # Carrega os dados direto do Google Drive
    df = pd.read_csv(URL_PLANILHA)
    
    busca = st.text_input("🔍 Digite o Nome ou Inforpen para buscar").upper()
    
    if busca:
        # Filtra em todas as colunas pelo que foi digitado
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
    st.info("Verifique se a planilha no Drive está como 'Qualquer pessoa com o link'.")
''')

# --- 4. EXECUÇÃO DO SISTEMA ---
# Inicia o Streamlit em segundo plano
subprocess.Popen(['streamlit', 'run', 'app.py', '--server.port', '8501'])
time.sleep(8)

# Gera o link de acesso (Procure pelo link terminado em .trycloudflare.com)
!./cloudflared tunnel --url http://localhost:8501
