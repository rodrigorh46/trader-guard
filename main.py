import streamlit as st
import streamlit.components.v1 as components
import time, hashlib, hmac, requests

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Trader Guard", layout="wide")

# --- CSS: LOGOTIPO E BOTÕES ---
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

# --- CONEXÃO BINANCE ---
def get_balance():
    try:
        api = st.secrets["binance"]["api_key"]
        sec = st.secrets["binance"]["api_secret"]
        ts = int(time.time() * 1000)
        query = f"timestamp={ts}"
        sig = hmac.new(sec.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
        res = requests.get(f"https://fapi.binance.com/fapi/v2/balance?{query}&signature={sig}", headers={'X-MBX-APIKEY': api}).json()
        return float(next(i['balance'] for i in res if i['asset'] == 'USDT'))
    except: return 0.0

saldo = get_balance()

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown('<div class="logo-container"><img src="https://cdn-icons-png.flaticon.com/512/2092/2092141.png" class="logo-img"><div class="logo-text">TRADER GUARD</div></div>', unsafe_allow_html=True)
    menu = st.radio("Navegação", ["🔴 Terminal", "💰 Depósito PIX", "💸 Saque PIX", "👤 Conta"])
    st.divider()
    # AGORA COM ADA E DOGE INCLUÍDAS
    moeda = st.selectbox("Escolha a Moeda:", ["BTCUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT"])
    
    if saldo > 0: st.success("✅ CONECTADO")
    else: st.error("⚠️ ATIVE 'FUTUROS' NA API BINANCE")

# --- TELAS ---
if menu == "🔴 Terminal":
    c1, c2 = st.columns([3, 1])
    with c1:
        components.html(f'<div style="height:620px;"><div id="tv"></div><script src="https://s3.tradingview.com/tv.js"></script><script>new TradingView.widget({{"width": "100%", "height": 620, "symbol": "BINANCE:{moeda}", "interval": "1", "theme": "dark", "style": "1", "locale": "br", "container_id": "tv"}});</script></div>', height=630)
    with c2:
        st.subheader("Execução")
        st.metric("Saldo USDT", f"$ {saldo:,.2f}")
        margem = st.number_input("Margem (R$)", value=100.0)
        alavanca = st.slider("Alavancagem", 1, 125, 10)
        if st.button("🚀 COMPRAR (LONG)"): st.success("Enviado!")
        if st.button("📉 VENDEDOR (CURTO)"): st.error("Enviado!")

elif menu == "💰 Depósito PIX":
    st.title("Depósito Instantâneo")
    valor = st.number_input("Valor (R$)", min_value=10.0, value=50.0)
    if st.button("Gerar QR Code"):
        # Simulador de QR Code
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=00020126360014br.gov.bcb.pix0114suachavepix{valor}")
        st.code("suachavepix@aqui.com", language="text")
        st.info("Após pagar, o saldo cai em até 5 minutos.")
