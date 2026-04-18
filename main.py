import streamlit as st
import streamlit.components.v1 as components
from binance.client import Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard", layout="wide", page_icon="🛡️")

# --- CSS PARA ESTILO E LOGOTIPO ORIGINAL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Logotipo de Circuito/Tecnologia que você gosta */
    .logo-container {
        text-align: center;
        padding: 15px;
        background: rgba(0, 212, 255, 0.05);
        border-radius: 10px;
        border: 1px solid #00d4ff;
        margin-bottom: 20px;
    }
    .logo-img {
        width: 70px;
        filter: drop-shadow(0px 0px 10px #00d4ff);
    }
    .logo-text {
        color: #00d4ff;
        font-family: 'Inter', sans-serif;
        font-size: 22px;
        font-weight: bold;
        margin-top: 10px;
        text-transform: uppercase;
    }

    /* Estilo dos Botões de Execução */
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        font-size: 16px !important;
    }
    /* Botão de Compra (Verde) */
    .stButton button:has(div p:contains("COMPRAR")) {
        background-color: #00c853 !important;
        color: white !important;
    }
    /* Botão de Vendedor (Vermelho) */
    .stButton button:has(div p:contains("VENDEDOR")) {
        background-color: #ff3d00 !important;
        color: white !important;
    }
    /* Botão de Sair (Laranja de Destaque) */
    .stButton button:has(div p:contains("FECHAR")) {
        background-color: #ff9800 !important;
        color: white !important;
        border: 2px solid white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A BINANCE ---
try:
    api_key = st.secrets["binance"]["api_key"]
    api_secret = st.secrets["binance"]["api_secret"]
    client = Client(api_key, api_secret)
    
    # Busca saldo real
    info = client.get_asset_balance(asset='USDT')
    saldo_real = float(info['free'])
    conectado = True
except Exception:
    saldo_real = 0.00
    conectado = False

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # O LOGOTIPO QUE PARECE UM VÍRUS VOLTOU
    st.markdown("""
    <div class="logo-container">
        <img src="https://cdn-icons-png.flaticon.com/512/2092/2092141.png" class="logo-img">
        <div class="logo-text">Trader Guard</div>
        <p style="color: #8b949e; font-size: 10px;">SECURITY & HIGH FREQUENCY</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("Navegação")
    menu = st.radio("", ["🔴 Operacional", "💰 Depósito PIX", "💸 Saque PIX", "👤 Minha Conta"], label_visibility="collapsed")
    
    st.divider()
    if conectado:
        st.success("✅ CONECTADO À BINANCE")
    else:
        st.warning("⚠️ MODO VISUALIZAÇÃO")
    
    st.info("📍 Servidor: Campina Grande - PB")

# --- PAINEL PRINCIPAL ---
col_graf, col_exec = st.columns([3, 1])

with col_graf:
    # Gráfico do TradingView
    tv_html = """
    <div style="height:620px;">
        <div id="tv_chart"></div>
        <script src="https://s3.tradingview.com/tv.js"></script>
        <script>
        new TradingView.widget({
          "width": "100%", "height": 620, "symbol": "BINANCE:BTCUSDT",
          "interval": "1", "theme": "dark", "style": "1", "locale": "br",
          "container_id": "tv_chart", "hide_side_toolbar": false
        });
        </script>
    </div>"""
    components.html(tv_html, height=630)

with col_exec:
    st.subheader("⚡ Execução")
    st.metric("Saldo Disponível (USDT)", f"$ {saldo_real:,.2f}")
    
    st.divider()
    
    # CONTROLES DE OPERAÇÃO QUE TINHAM SUMIDO
    margem = st.number_input("Margem (R$)", min_value=10.0, value=100.0, step=10.0)
    alavancagem = st.slider("Alavancagem", 1, 125, 10)
    
    st.write("")
    
    # Botões de Ação
    if st.button("🚀 COMPRAR (LONG)"):
        st.success(f"Ordem de COMPRA enviada!")
        
    if st.button("📉 VENDEDOR (CURTO)"):
        st.error(f"Ordem de VENDA enviada!")
        
    st.write("")
    
    # O BOTÃO DE SAIR QUE VOCÊ PEDIU
    if st.button("⏹️ FECHAR POSIÇÃO AGORA"):
        st.warning("⚠️ Encerrando todas as ordens abertas...")
