import streamlit as st
import streamlit.components.v1 as components
import time, hashlib, hmac, requests

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Trader Guard", layout="wide")

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .logo-container { text-align: center; padding: 20px; border: 2px solid #00d4ff; border-radius: 15px; margin-bottom: 25px; }
    .logo-text { color: #00d4ff; font-size: 24px; font-weight: bold; }
    div.stButton > button { width: 100% !important; height: 50px !important; font-weight: bold !important; border-radius: 10px !important; }
    .stButton button:has(div p:contains("COMPRAR")) { background-color: #00c853 !important; color: white !important; }
    .stButton button:has(div p:contains("VENDEDOR")) { background-color: #ff3d00 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A BINANCE (CORRIGIDA) ---
def get_balance():
    try:
        api = st.secrets["binance"]["api_key"]
        sec = st.secrets["binance"]["api_secret"]
        ts = int(time.time() * 1000)
        query = f"timestamp={ts}"
        sig = hmac.new(sec.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
        url = f"https://fapi.binance.com/fapi/v2/balance?{query}&signature={sig}"
        res = requests.get(url, headers={'X-MBX-APIKEY': api}, timeout=10).json()
        for item in res:
            if item['asset'] == 'USDT': return float(item['balance'])
    except: return 0.0
    return 0.0

saldo = get_balance()

# --- MENU LATERAL ---
with st.sidebar:
    st.markdown('<div class="logo-container"><div class="logo-text">🛡️ TRADER GUARD</div></div>', unsafe_allow_html=True)
    menu = st.radio("Navegação", ["🔴 Terminal", "💰 Depósito PIX", "💸 Saque PIX", "👤 Conta"])
    st.divider()
    # MOEDAS ADICIONADAS: ADA E DOGE
    moeda = st.selectbox("Moeda para Operar:", ["BTCUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT"])
    st.divider()
    if saldo > 0: st.success(f"✅ CONECTADO: $ {saldo:,.2f}")
    else: st.error("⚠️ ERRO: ATIVE 'FUTUROS' NA BINANCE")

# --- TELAS ---
if menu == "🔴 Terminal":
    c1, c2 = st.columns([3, 1])
    with c1:
        components.html(f'<div style="height:620px;"><div id="tv"></div><script src="https://s3.tradingview.com/tv.js"></script><script>new TradingView.widget({{"width": "100%", "height": 620, "symbol": "BINANCE:{moeda}", "interval": "1", "theme": "dark", "style": "1", "locale": "br", "container_id": "tv"}});</script></div>', height=630)
    with c2:
        st.subheader("Painel de Ordem")
        st.metric("Saldo Atual (USDT)", f"$ {saldo:,.2f}")
        st.number_input("Margem (R$)", value=100.0)
        st.slider("Alavancagem", 1, 125, 20)
        st.button("🚀 COMPRAR (LONG)")
        st.button("📉 VENDEDOR (CURTO)")

elif menu == "💰 Depósito PIX":
    st.title("Depósito via PIX")
    valor_pix = st.number_input("Valor para Depósito (R$)", min_value=10.0, value=50.0)
    if st.button("Gerar Código PIX"):
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=PIX_CHAVE_EXEMPLO_{valor_pix}")
        st.code("suachavepix@aqui.com", language="text")
        st.info("O saldo será creditado após a confirmação bancária.")
