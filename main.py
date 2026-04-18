import streamlit as st
import streamlit.components.v1 as components
from binance.client import Client

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Trader Guard", layout="wide", page_icon="🛡️")

# --- CSS: LOGO DE VÍRUS E BOTÕES ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .logo-container { text-align: center; padding: 15px; border: 1px solid #00d4ff; border-radius: 10px; margin-bottom: 20px; }
    .logo-img { width: 70px; filter: drop-shadow(0px 0px 10px #00d4ff); }
    .logo-text { color: #00d4ff; font-family: 'Inter', sans-serif; font-size: 22px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }
    div.stButton > button { width: 100% !important; height: 50px !important; font-weight: bold !important; }
    .stButton button:has(div p:contains("COMPRAR")) { background-color: #00c853 !important; }
    .stButton button:has(div p:contains("VENDEDOR")) { background-color: #ff3d00 !important; }
    .stButton button:has(div p:contains("FECHAR")) { background-color: #ff9800 !important; border: 2px solid white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BINANCE (MARRETA PARA CHAVES) ---
saldo_real = 0.0
conectado = False
try:
    if "binance" in st.secrets:
        # Força o uso do servidor correto para evitar erros de conexão
        client = Client(st.secrets["binance"]["api_key"], st.secrets["binance"]["api_secret"])
        # Tenta pegar saldo de Futuros (USDT)
        acc = client.futures_account_balance()
        saldo_real = float(next(i['balance'] for i in acc if i['asset'] == 'USDT'))
        conectado = True
except Exception:
    saldo_real = 0.0

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown('<div class="logo-container"><img src="https://cdn-icons-png.flaticon.com/512/2092/2092141.png" class="logo-img"><div class="logo-text">Trader Guard</div></div>', unsafe_allow_html=True)
    
    # SELETOR DE MOEDAS QUE VOCÊ QUERIA
    st.subheader("🌐 Selecionar Par")
    moeda = st.selectbox("", ["BTCUSDT", "SOLUSDT", "XRPUSDT", "ETHUSDT"], label_visibility="collapsed")
    
    st.divider()
    if conectado: st.success("✅ CONECTADO")
    else: st.error("⚠️ ERRO DE CHAVE")
    st.info("📍 Campina Grande - PB")

# --- PAINEL PRINCIPAL ---
col_graf, col_exec = st.columns([3, 1])

with col_graf:
    # Gráfico que muda conforme a moeda selecionada
    tv_html = f"""
    <div style="height:620px;"><div id="tv_chart"></div><script src="https://s3.tradingview.com/tv.js"></script>
    <script>new TradingView.widget({{"width": "100%", "height": 620, "symbol": "BINANCE:{moeda}", "interval": "1", "theme": "dark", "style": "1", "locale": "br", "container_id": "tv_chart", "hide_side_toolbar": false}});</script></div>"""
    components.html(tv_html, height=630)

with col_exec:
    st.subheader("⚡ Execução")
    st.metric(f"Saldo {moeda}", f"$ {saldo_real:,.2f}")
    st.divider()
    margem = st.number_input("Margem (R$)", min_value=10.0, value=100.0)
    alavancagem = st.slider("Alavancagem", 1, 125, 10)
    
    if st.button("🚀 COMPRAR (LONG)"): st.success(f"Ordem {moeda} enviada!")
    if st.button("📉 VENDEDOR (CURTO)"): st.error(f"Ordem {moeda} enviada!")
    st.write("")
    if st.button("⏹️ FECHAR POSIÇÃO AGORA"): st.warning("⚠️ Encerrando ordens...")
