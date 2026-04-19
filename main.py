import streamlit as st
import streamlit.components.v1 as components
from binance.client import Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard ELITE 🛡️", layout="wide", page_icon="🛡️")

# --- CSS PARA ESTILIZAÇÃO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .logo-text { color: #00d4ff; font-size: 32px; font-weight: 800; }
    .logo-sub { color: #8b949e; font-size: 12px; text-transform: uppercase; }
    div.stButton > button:first-child { width: 100%; height: 50px; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE VARIÁVEIS ---
saldo_real = 0.0
status_conexao = "⚠️ AGUARDANDO CONFIGURAÇÃO"

# --- CONEXÃO SEGURA COM PROXY E BINANCE ---
try:
    # 1. Puxa os dados do Proxy dos Secrets (Protegido)
    px_user = st.secrets["proxy"]["user"]
    px_pass = st.secrets["proxy"]["pass"]
    px_ip   = st.secrets["proxy"]["ip"]
    px_port = st.secrets["proxy"]["port"]

    proxies = {
        'http': f'http://{px_user}:{px_pass}@{px_ip}:{px_port}',
        'https': f'http://{px_user}:{px_pass}@{px_ip}:{px_port}'
    }

    # 2. Puxa as chaves da Binance dos Secrets
    api_key = st.secrets["binance"]["api_key"]
    api_secret = st.secrets["binance"]["api_secret"]

    # 3. Inicia o Client com o túnel do Proxy
    client = Client(api_key, api_secret, requests_params={'proxies': proxies, 'timeout': 15})
    client.API_URL = 'https://api.binance.com/api' # Força endpoint global

    # 4. Busca saldo de Futuros
    info = client.futures_account_balance()
    saldo_usdt = next((item for item in info if item['asset'] == 'USDT'), None)
    
    if saldo_usdt:
        saldo_real = float(saldo_usdt['balance'])
        status_conexao = "✅ ONLINE (VIA PROXY SEGURO)"

except KeyError:
    status_conexao = "❌ ERRO: Configure os SECRETS no Streamlit Cloud"
except Exception as e:
    status_conexao = f"❌ ERRO DE CONEXÃO: {str(e)}"

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
    st.info(f"📍 Servidor: HostGator (Túnel Brasil)")

# --- TERMINAL DE TRADE ---
if menu == "📈 Terminal de Trade":
    col_graf, col_painel = st.columns([3, 1])

    with col_graf:
        tv_html = """
        <div style="height:620px;"><div id="chart_div"></div>
        <script src="https://s3.tradingview.com/tv.js"></script>
        <script>
        new TradingView.widget({
            "width": "100%", "height": 620, "symbol": "BINANCE:BTCUSDT.P",
            "interval": "1", "theme": "dark", "style": "1", "locale": "br",
            "container_id": "chart_div", "hide_side_toolbar": false, "allow_symbol_change": true
        });
        </script></div>"""
        components.html(tv_html, height=630)

    with col_painel:
        st.subheader("⚡ Boleta de Ordem")
        st.metric("Saldo (USDT)", f"$ {saldo_real:,.2f}")
        st.divider()
        
        margem = st.number_input("Entrada ($)", min_value=5.0, value=20.0)
        alavanca = st.slider("Alavancagem", 1, 50, 10)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 COMPRAR"):
                st.toast("Enviando LONG via Proxy...")
        with c2:
            if st.button("📉 VENDER"):
                st.toast("Enviando SHORT via Proxy...")
        
        if st.button("⏹️ FECHAR POSIÇÃO AGORA", type="primary"):
            try:
                client.futures_cancel_all_open_orders(symbol='BTCUSDT')
                st.warning("Ordens canceladas!")
            except:
                st.error("Falha ao fechar.")

elif menu == "💰 Gestão PIX":
    st.title("Depósitos Granpolid")
    st.write("Módulo de pagamentos seguro.")

elif menu == "👤 Perfil API":
    st.title("Segurança da Conta")
    st.info(f"Status Atual: {status_conexao}")
