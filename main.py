import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import hashlib
import hmac
import time
import requests

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Trader Guard", layout="wide")

# --- CSS: LOGO DE VÍRUS E BOTÕES ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .logo-container { text-align: center; padding: 15px; border: 1px solid #00d4ff; border-radius: 10px; margin-bottom: 20px; }
    .logo-img { width: 70px; filter: drop-shadow(0px 0px 10px #00d4ff); }
    .logo-text { color: #00d4ff; font-family: 'Inter', sans-serif; font-size: 20px; font-weight: bold; }
    div.stButton > button { width: 100% !important; height: 50px !important; font-weight: bold !important; }
    .stButton button:has(div p:contains("COMPRAR")) { background-color: #00c853 !important; }
    .stButton button:has(div p:contains("VENDEDOR")) { background-color: #ff3d00 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PARA PEGAR SALDO (SEM BUG) ---
def get_binance_balance():
    try:
        api_key = st.secrets["binance"]["api_key"]
        secret = st.secrets["binance"]["api_secret"]
        base_url = "https://fapi.binance.com"
        endpoint = "/fapi/v2/balance"
        timestamp = int(time.time() * 1000)
        query_string = f"timestamp={timestamp}"
        signature = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = f"{base_url}{endpoint}?{query_string}&signature={signature}"
        headers = {'X-MBX-APIKEY': api_key}
        res = requests.get(url, headers=headers).json()
        for asset in res:
            if asset['asset'] == 'USDT':
                return float(asset['balance'])
    except:
        return 0.0
    return 0.0

saldo = get_binance_balance()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="logo-container"><img src="https://cdn-icons-png.flaticon.com/512/2092/2092141.png" class="logo-img"><div class="logo-text">TRADER GUARD</div></div>', unsafe_allow_html=True)
    menu = st.radio("Menu", ["🔴 Operacional", "💰 Depósito PIX", "💸 Saque PIX", "👤 Minha Conta"])
    st.divider()
    # AGORA COM ADA E DOGE
    moeda = st.selectbox("Operar Moeda:", ["BTCUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT"])
    
    if saldo > 0: st.success("✅ CHAVES ATIVAS")
    else: st.error("⚠️ ERRO: ATIVE 'FUTUROS' NA BINANCE")

# --- TELAS ---
if menu == "🔴 Operacional":
    c1, c2 = st.columns([3, 1])
    with c1:
        components.html(f'<div style="height:620px;"><div id="tv"></div><script src="https://s3.tradingview.com/tv.js"></script><script>new TradingView.widget({{"width": "100%", "height": 620, "symbol": "BINANCE:{moeda}", "interval": "1", "theme": "dark", "style": "1", "locale": "br", "container_id": "tv"}});</script></div>', height=630)
    with c2:
        st.subheader("Execução")
        st.metric("Saldo USDT", f"$ {saldo:,.2f}")
        st.number_input("Margem (R$)", value=100.0)
        st.slider("Alavancagem", 1, 125, 10)
        st.button("🚀 COMPRAR (LONG)")
        st.button("📉 VENDEDOR (CURTO)")

elif menu == "💰 Depósito PIX":
    st.title("Depósito via PIX")
    st.write("Copie a chave abaixo para depositar:")
    st.code("suachavepix@aqui.com", language="text")
    st.warning("O sistema de QR Code automático está em manutenção.")
