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
    .stButton button:has(div p:contains("Fechar")) { background-color: #1e1e1e !important; color: #00d4ff !important; border: 2px solid #00d4ff !important; }
    @keyframes pulse {
        0% { box-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff; }
        50% { box-shadow: 0 0 20px #00d4ff, 0 0 40px #00d4ff; }
        100% { box-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff; }
    }
    .pulse-logo {
        animation: pulse 2s infinite;
        border-radius: 50%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A BINANCE (CORRIGIDA) ---
def get_balance():
    try:
        api = st.secrets["binance"]["api_key"]
        sec = st.secrets["binance"]["api_secret"]
        ts = int(time.time() * 1000)
        query = f"timestamp={ts}&recvWindow=5000"
        sig = hmac.new(sec.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
        url = f"https://fapi.binance.com/fapi/v2/balance?{query}&signature={sig}"
        res = requests.get(url, headers={'X-MBX-APIKEY': api}, timeout=10).json()
        if isinstance(res, list):
            for item in res:
                if item.get('asset') == 'USDT':
                    return float(item.get('balance', 0.0))
        return 0.0
    except Exception as e:
        st.error(f"Erro na API: {e}")
        return 0.0

saldo = get_balance()

# --- MENU LATERAL ---
with st.sidebar:
    st.markdown('<div class="logo-container"><img src="https://copilot.microsoft.com/th/id/BCO.be6a8e45-0b24-42a7-92da-506929719f2b.png" width="120" class="pulse-logo"><div class="logo-text">🛡️ TRADER GUARD</div></div>', unsafe_allow_html=True)
    menu = st.radio("Navegação", ["🔴 Terminal", "💰 Depósito PIX", "💸 Saque PIX", "👤 Conta"])
    st.divider()
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
        st.button("❌ Fechar Operação")

elif menu == "💰 Depósito PIX":
    st.title("Depósito via PIX")
    valor_pix = st.number_input("Valor para Depósito (R$)", min_value=10.0, value=50.0)
    if st.button("Gerar Código PIX"):
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=PIX_CHAVE_EXEMPLO_{valor_pix}")
        st.code("suachavepix@aqui.com", language="text")
        st.info("O saldo será creditado após a confirmação bancária.")
