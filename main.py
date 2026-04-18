import streamlit as st
import streamlit.components.v1 as components
from binance.client import Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard ELITE 🛡️", layout="wide", page_icon="🛡️")

# --- CSS PARA O SEU LOGOTIPO (AGORA FIXO!) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* O SEU LOGOTIPO VOLTOU AQUI */
    .logo-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00d4ff;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 0px 20px rgba(0, 212, 255, 0.2);
    }
    .logo-shield { font-size: 40px; margin-bottom: 10px; }
    .logo-text {
        color: #00d4ff;
        font-family: 'Arial Black', sans-serif;
        font-size: 22px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
        text-shadow: 0px 0px 10px rgba(0, 212, 255, 0.6);
    }
    .logo-tag { color: #94a3b8; font-size: 10px; letter-spacing: 2px; }

    /* Estilo dos Botões e Status */
    div.stButton > button { width: 100% !important; height: 50px !important; border-radius: 10px !important; }
    .stMetric { background: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A BINANCE ---
try:
    api_key = st.secrets["binance"]["api_key"]
    api_secret = st.secrets["binance"]["api_secret"]
    client = Client(api_key, api_secret)
    
    # Puxa saldo real (Spot)
    conta = client.get_asset_balance(asset='USDT')
    saldo_real = float(conta['free'])
    
    status_conexao = "✅ SISTEMA CONECTADO"
    modo_visualizacao = False
except Exception:
    saldo_real = 0.0
    status_conexao = "⚠️ MODO VISUALIZAÇÃO"
    modo_visualizacao = True
    api_key = "Chave não encontrada"

# --- SIDEBAR (BARRA LATERAL) ---
with st.sidebar:
    # AQUI ESTÁ O SEU LOGOTIPO RODRIGO!
    st.markdown(f"""
    <div class="logo-box">
        <div class="logo-shield">🛡️</div>
        <p class="logo-text">TRADER GUARD</p>
        <p class="logo-tag">SECURITY & HIGH FREQUENCY</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Navegação Principal", ["📈 Terminal de Trade", "💰 Gestão PIX", "👤 Perfil API"])
    st.divider()
    
    if modo_visualizacao: st.warning(status_conexao)
    else: st.success(status_conexao)
    
    st.info(f"📍 Servidor: Campina Grande - PB")

# --- CONTEÚDO PRINCIPAL ---
if menu == "📈 Terminal de Trade":
    col_graf, col_painel = st.columns([3, 1])

    with col_graf:
        # Gráfico do TradingView
        tv_html = """
        <div style="height:620px;">
            <div id="chart_div"></div>
            <script src="https://s3.tradingview.com/tv.js"></script>
            <script>
            new TradingView.widget({
                "width": "100%", "height": 620, "symbol": "BINANCE:BTCUSDT",
                "interval": "1", "theme": "dark", "style": "1", "locale": "br",
                "container_id": "chart_div", "hide_side_toolbar": false
            });
            </script>
        </div>"""
        components.html(tv_html, height=630)

    with col_painel:
        st.subheader("Boleta de Ordem")
        st.metric("Saldo na Binance (USDT)", f"$ {saldo_real:,.2f}")
        st.divider()
        
        if modo_visualizacao:
            st.error("Conecte suas chaves nos Secrets para operar.")
        else:
            margem = st.number_input("Entrada ($)", min_value=1.0, value=10.0)
            if st.button("🚀 COMPRAR"): st.success("Ordem de Compra!")
            if st.button("📉 VENDER"): st.error("Ordem de Venda!")
            if st.button("⏹️ FECHAR POSIÇÃO AGORA"): st.warning("Fechando...")

elif menu == "👤 Perfil API":
    st.title("Configurações")
    st.write(f"Sua API Key começa com: `{api_key[:10]}`")
