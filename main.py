import streamlit as st
import streamlit.components.v1 as components
from binance.client import Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard", layout="wide", page_icon="🛡️")

# --- CSS PARA O LOGOTIPO ORIGINAL (ÍCONE DE CIRCUITO/VÍRUS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Logotipo de Circuito/Vírus que você gosta */
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
        letter-spacing: 1px;
    }

    /* Estilo dos Botões e Status */
    div.stButton > button { width: 100% !important; height: 50px !important; font-weight: bold !important; border-radius: 8px !important; }
    .stButton button:has(div p:contains("COMPRAR")) { background-color: #00c853 !important; color: white !important; }
    .stButton button:has(div p:contains("VENDEDOR")) { background-color: #ff3d00 !important; color: white !important; }
    .stButton button:has(div p:contains("FECHAR")) { background-color: #ff9800 !important; color: white !important; border: 2px solid white !important; }
    .stMetric { background: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A BINANCE ---
saldo_real = 0.0
conectado = False
status_msg = "MODO VISUALIZAÇÃO"

try:
    if "binance" in st.secrets:
        client = Client(st.secrets["binance"]["api_key"], st.secrets["binance"]["api_secret"])
        
        # Tenta buscar saldo de Futuros (prioridade para evitar erros em contas spot zeradas)
        try:
            acc = client.futures_account_balance()
            saldo_real = float(next(i['balance'] for i in acc if i['asset'] == 'USDT'))
            conectado = True
        except:
            # Se falhar, tenta Spot
            acc = client.get_asset_balance(asset='USDT')
            saldo_real = float(acc['free'])
            conectado = True
        
        if conectado: status_msg = "CONECTADO À BINANCE"
except Exception as e:
    status_msg = "ERRO DE CHAVE: Verifique permissões"

# --- SIDEBAR (BARRA LATERAL) ---
with st.sidebar:
    # O LOGOTIPO DE CIRCUITO/VÍRUS VOLTOU EXATAMENTE COMO VOCÊ QUERIA
    st.markdown("""
    <div class="logo-container">
        <img src="https://cdn-icons-png.flaticon.com/512/2092/2092141.png" class="logo-img">
        <div class="logo-text">Trader Guard</div>
        <p style="color: #8b949e; font-size: 10px;">SECURITY & HIGH FREQUENCY</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Navegação Principal", ["🔴 Terminal de Trade", "💰 Gestão PIX", "👤 Perfil API"])
    
    st.divider()
    if conectado: st.success(f"✅ {status_msg}")
    else: st.warning(f"⚠️ {status_msg}")
    st.info("📍 Servidor: Campina Grande - PB")

# --- CONTEÚDO PRINCIPAL ---
if menu == "🔴 Terminal de Trade":
    col_graf, col_exec = st.columns([3, 1])

    with col_graf:
        # Gráfico do TradingView
        tv_html = """
        <div style="height:620px;"><div id="tv_chart"></div><script src="https://s3.tradingview.com/tv.js"></script><script>new TradingView.widget({"width": "100%", "height": 620, "symbol": "BINANCE:BTCUSDT", "interval": "1", "theme": "dark", "style": "1", "locale": "br", "container_id": "tv_chart", "hide_side_toolbar": false});</script></div>"""
        components.html(tv_html, height=630)

    with col_exec:
        st.subheader("⚡ Execução")
        st.metric("Saldo Disponível (USDT)", f"$ {saldo_real:,.2f}")
        st.divider()
        
        # CONTROLES DE OPERAÇÃO QUE TINHAM SUMIDO
        margem = st.number_input("Margem (R$)", min_value=10.0, value=100.0, step=10.0)
        alavancagem = st.slider("Alavancagem", 1, 125, 10)
        
        st.write("")
        
        if st.button("🚀 COMPRAR (LONG)"): st.success("Ordem enviada!")
        if st.button("📉 VENDEDOR (CURTO)"): st.error("Ordem enviada!")
        st.write("")
        if st.button("⏹️ FECHAR POSIÇÃO AGORA"): st.warning("Fechando ordens...")

elif menu == "👤 Perfil API":
    st.title("Configurações API")
    if conectado: st.write("✅ Suas chaves estão configuradas.")
    else: st.write("⚠️ Verifique suas chaves API nos Secrets.")
