import streamlit as st
import streamlit.components.v1 as components
from binance.client import Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard", layout="wide", page_icon="🛡️")

# --- CSS PARA ESTILO E LOGOTIPO ORIGINAL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .logo-container { text-align: center; padding: 15px; border: 1px solid #00d4ff; border-radius: 10px; margin-bottom: 20px; }
    .logo-img { width: 70px; filter: drop-shadow(0px 0px 10px #00d4ff); }
    .logo-text { color: #00d4ff; font-family: 'Inter', sans-serif; font-size: 22px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }
    div.stButton > button { width: 100% !important; height: 50px !important; font-weight: bold !important; border-radius: 8px !important; }
    .stButton button:has(div p:contains("COMPRAR")) { background-color: #00c853 !important; color: white !important; }
    .stButton button:has(div p:contains("VENDEDOR")) { background-color: #ff3d00 !important; color: white !important; }
    .stButton button:has(div p:contains("FECHAR")) { background-color: #ff9800 !important; color: white !important; border: 2px solid white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A BINANCE (TENTATIVA DUPLA) ---
saldo_real = 0.0
conectado = False
status_msg = "MODO VISUALIZAÇÃO"

try:
    if "binance" in st.secrets:
        api_key = st.secrets["binance"]["api_key"]
        api_secret = st.secrets["binance"]["api_secret"]
        client = Client(api_key, api_secret)
        
        # Tenta buscar saldo Spot primeiro
        try:
            info = client.get_asset_balance(asset='USDT')
            if info: saldo_real = float(info['free'])
            conectado = True
        except:
            # Se falhar, tenta buscar saldo de Futuros
            info = client.futures_account_balance()
            item = next((i for i in info if i['asset'] == 'USDT'), None)
            if item: saldo_real = float(item['balance'])
            conectado = True
            
        if conectado: status_msg = "CONECTADO À BINANCE"
except Exception as e:
    status_msg = f"ERRO: {str(e)[:20]}"

# --- BARRA LATERAL ---
with st.sidebar:
    # O LOGOTIPO QUE PARECE UM VÍRUS/CIRCUITO VOLTOU
    st.markdown("""
    <div class="logo-container">
        <img src="https://cdn-icons-png.flaticon.com/512/2092/2092141.png" class="logo-img">
        <div class="logo-text">Trader Guard</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("Navegação")
    st.radio("", ["🔴 Operacional", "💰 Depósito PIX", "💸 Saque PIX", "👤 Minha Conta"], label_visibility="collapsed")
    
    st.divider()
    if conectado: st.success(f"✅ {status_msg}")
    else: st.warning(f"⚠️ {status_msg}")
    st.info("📍 Servidor: Campina Grande - PB")

# --- PAINEL PRINCIPAL ---
col_graf, col_exec = st.columns([3, 1])

with col_graf:
    tv_html = """
    <div style="height:620px;"><div id="tv_chart"></div><script src="https://s3.tradingview.com/tv.js"></script>
    <script>new TradingView.widget({"width": "100%", "height": 620, "symbol": "BINANCE:BTCUSDT", "interval": "1", "theme": "dark", "style": "1", "locale": "br", "container_id": "tv_chart", "hide_side_toolbar": false});</script></div>"""
    components.html(tv_html, height=630)

with col_exec:
    st.subheader("⚡ Execução")
    st.metric("Saldo Disponível (USDT)", f"$ {saldo_real:,.2f}")
    st.divider()
    margem = st.number_input("Margem (R$)", min_value=10.0, value=100.0, step=10.0)
    alavancagem = st.slider("Alavancagem", 1, 125, 10)
    
    if st.button("🚀 COMPRAR (LONG)"): st.success("Ordem enviada!")
    if st.button("📉 VENDEDOR (CURTO)"): st.error("Ordem enviada!")
    st.write("")
    if st.button("⏹️ FECHAR POSIÇÃO AGORA"): st.warning("⚠️ Encerrando ordens...")
