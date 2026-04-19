import streamlit as st
import streamlit.components.v1 as components
from binance.client import Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard ELITE 🛡️", layout="wide", page_icon="🛡️")

# Inicialização de variáveis para evitar NameError
saldo_real = 0.0
api_key = "Não Configurada"
status_conexao = "⚠️ MODO VISUALIZAÇÃO"

# --- CSS PARA ESTILIZAÇÃO AVANÇADA ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .logo-text {
        font-family: 'Inter', sans-serif;
        color: #00d4ff;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0px;
        text-shadow: 0px 0px 15px rgba(0, 212, 255, 0.4);
    }
    .logo-sub {
        color: #8b949e;
        font-size: 12px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }
    div.stButton > button:first-child {
        width: 100%;
        height: 50px;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A BINANCE ---
try:
    if "binance" in st.secrets:
        api_key = st.secrets["binance"]["api_key"]
        api_secret = st.secrets["binance"]["api_secret"]
        client = Client(api_key, api_secret)
        
        # Obtendo saldo de Futuros
        info = client.futures_account_balance()
        # Filtra o ativo USDT com segurança
        saldo_usdt = next((item for item in info if item['asset'] == 'USDT'), None)
        if saldo_usdt:
            saldo_real = float(saldo_usdt['balance'])
            status_conexao = "✅ SISTEMA ONLINE"
    else:
        status_conexao = "⚠️ SECRETS NÃO CONFIGURADAS"
except Exception as e:
    status_conexao = f"❌ ERRO: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<p class="logo-text">🛡️ TRADER GUARD</p>', unsafe_allow_html=True)
    st.markdown('<p class="logo-sub">Security & High Frequency Trading</p>', unsafe_allow_html=True)
    
    menu = st.radio("Navegação Principal", ["📈 Terminal de Trade", "💰 Gestão PIX", "👤 Perfil API"])
    
    st.divider()
    if "✅" in status_conexao:
        st.success(status_conexao)
    else:
        st.error(status_conexao)
    st.info(f"📍 Servidor: Campina Grande - PB")

# --- CONTEÚDO PRINCIPAL ---
if menu == "📈 Terminal de Trade":
    col_graf, col_painel = st.columns([3, 1])

    with col_graf:
        tv_html = """
        <div style="height:620px;">
            <div id="chart_div"></div>
            <script src="https://s3.tradingview.com/tv.js"></script>
            <script>
            new TradingView.widget({
                "width": "100%", "height": 620, "symbol": "BINANCE:BTCUSDT.P",
                "interval": "1", "theme": "dark", "style": "1", "locale": "br",
                "container_id": "chart_div", "hide_side_toolbar": false, "allow_symbol_change": true
            });
            </script>
        </div>"""
        components.html(tv_html, height=630)

    with col_painel:
        st.subheader("⚡ Boleta de Ordem")
        st.metric("Saldo Disponível (USDT)", f"$ {saldo_real:,.2f}", delta="Ao Vivo")
        st.divider()
        
        margem = st.number_input("Valor da Entrada ($)", min_value=5.0, value=20.0, step=5.0)
        alavanca = st.slider("Alavancagem", 1, 50, 10)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 COMPRAR"):
                st.toast(f"Ordem de LONG enviada: ${margem}")
        with col_btn2:
            if st.button("📉 VENDER"):
                st.toast(f"Ordem de SHORT enviada: ${margem}")
        
        st.write("") 
        
        if st.button("⏹️ FECHAR POSIÇÃO AGORA", type="primary"):
            st.warning("⚠️ Encerrando todas as ordens abertas...")

elif menu == "💰 Gestão PIX":
    st.title("Depósitos e Saques")
    st.info("Integração via API Gateway em desenvolvimento.")

elif menu == "👤 Perfil API":
    st.title("Configurações de Segurança")
    # Exibe parte da chave apenas se ela existir
    if api_key != "Não Configurada":
        st.code(f"API KEY: {api_key[:10]}****************")
    else:
        st.warning("Nenhuma API Key detectada nos Secrets.")
