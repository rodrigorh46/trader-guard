import streamlit as st
import streamlit.components.v1 as components
from binance.client import Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard ELITE 🛡️", layout="wide", page_icon="🛡️")

# --- CSS PARA ESTILIZAÇÃO AVANÇADA ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    /* Estilo do Logotipo */
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
    /* Botões Customizados */
    div.stButton > button:first-child {
        width: 100%;
        height: 50px;
        font-weight: bold;
        border-radius: 10px;
    }
    /* Botão de Fechar Operação */
    .stButton button:has(div p:contains("FECHAR")) {
        background-color: #ff9800 !important;
        color: white !important;
        border: none !important;
    }
    .stButton button:hover:has(div p:contains("FECHAR")) {
        background-color: #e68900 !important;
        box-shadow: 0px 0px 15px rgba(255, 152, 0, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A BINANCE ---
try:
    api_key = st.secrets["binance"]["api_key"]
    api_secret = st.secrets["binance"]["api_secret"]
    client = Client(api_key, api_secret)
    
    # Puxando o saldo real de USDT (Dólar) para Futuros
    # Se quiser Spot, mude para: client.get_asset_balance(asset='USDT')
    info = client.futures_account_balance()
    saldo_usdt = next(item for item in info if item['asset'] == 'USDT')
    saldo_real = float(saldo_usdt['balance'])
    
    status_conexao = "✅ SISTEMA ONLINE"
except Exception:
    saldo_real = 0.0
    status_conexao = "⚠️ MODO VISUALIZAÇÃO"

# --- SIDEBAR (BARRA LATERAL) ---
with st.sidebar:
    # Logotipo Melhorado
    st.markdown('<p class="logo-text">🛡️ TRADER GUARD</p>', unsafe_allow_html=True)
    st.markdown('<p class="logo-sub">Security & High Frequency Trading</p>', unsafe_allow_html=True)
    
    menu = st.radio("Navegação Principal", ["📈 Terminal de Trade", "💰 Gestão PIX", "👤 Perfil API"])
    
    st.divider()
    st.success(status_conexao)
    st.info(f"📍 Servidor: Campina Grande - PB")

# --- CONTEÚDO PRINCIPAL ---
if menu == "📈 Terminal de Trade":
    col_graf, col_painel = st.columns([3, 1])

    with col_graf:
        # Gráfico do TradingView (BTC/USDT Futuros)
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
        
        # Dashboard de Saldo
        st.metric("Saldo Disponível (USDT)", f"$ {saldo_real:,.2f}", delta="Ao Vivo")
        
        st.divider()
        
        # Controles de Operação
        margem = st.number_input("Valor da Entrada ($)", min_value=5.0, value=20.0, step=5.0)
        alavanca = st.slider("Alavancagem", 1, 50, 10)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 COMPRAR"):
                st.toast(f"Ordem de LONG enviada: ${margem}")
        with col_btn2:
            if st.button("📉 VENDER"):
                st.toast(f"Ordem de SHORT enviada: ${margem}")
        
        st.write("") # Espaçamento
        
        # BOTÃO DE SAIR DA OPERAÇÃO (O que você pediu)
        if st.button("⏹️ FECHAR POSIÇÃO AGORA"):
            st.warning("⚠️ Encerrando todas as ordens abertas...")
            # Aqui entraria a função: client.futures_cancel_all_open_orders(symbol='BTCUSDT')

elif menu == "💰 Gestão PIX":
    st.title("Depósitos e Saques")
    st.write("Funcionalidade em integração com o gateway de pagamento.")

elif menu == "👤 Perfil API":
    st.title("Configurações de Segurança")
    st.write(f"Conectado à chave: `{api_key[:10]}...`")
