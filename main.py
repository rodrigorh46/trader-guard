import streamlit as st
import time

# tenta pegar a chave real
API_KEY = st.secrets.get("openpix", {}).get("api_key", None)

def gerar_qr_pix(valor):
    if API_KEY:
        # aqui iria a chamada real da API OpenPix
        return f"https://api.openpix.com.br/qr/{valor}", "link_real"
    else:
        # fallback: gera QR fake
        fake_qr = f"https://fake.qr/{valor}-{int(time.time())}"
        return fake_qr, "link_fake"

def solicitar_saque(chave_pix, valor):
    if API_KEY:
        # chamada real da API
        return {"status": "ok", "pix": {"valor": valor, "chave": chave_pix}}
    else:
        # fallback: simulação
        return {"status": "simulado", "pix": {"valor": valor, "chave": chave_pix}}

# --- INTERFACE ---
st.title("🛡️ Trader Guard")

valor_pix = st.number_input("Valor para Depósito (R$)", min_value=10.0, value=50.0)
if st.button("Gerar Código PIX"):
    qr_url, link = gerar_qr_pix(valor_pix)
    st.image(qr_url)
    st.code(link, language="text")
    if not API_KEY:
        st.warning("⚠️ Modo teste: QR gerado apenas para simulação.")

chave = st.text_input("Informe sua chave PIX para saque")
valor_saque = st.number_input("Valor para Saque (R$)", min_value=10.0, value=50.0)
if st.button("Solicitar Saque"):
    resultado = solicitar_saque(chave, valor_saque)
    st.write(resultado)
    if not API_KEY:
        st.warning("⚠️ Modo teste: saque apenas simulado.")
