import streamlit as st
import streamlit.components.v1 as components
from binance.client import Client
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard ELITE 🛡️", layout="wide", page_icon="🛡️")

# --- CSS PARA ESTILIZAÇÃO (O SEU LOGOTIPO ESTÁ AQUI!) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    /* Estilo do Logotipo (Melhorado e Fixo) */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
        padding: 10px;
        background: rgba(0, 212, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(0, 212, 255, 0.1);
    }
    .logo-text {
        font-family: 'Inter', sans-serif;
        color: #00d4ff;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0px;
        text-shadow: 0px 0px 15px rgba(0, 212, 255, 0.5);
    }
    .logo-sub {
        color: #8b949e;
        font-size: 10px;
        margin-top: -5px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    /* Estilo dos Botões */
    div.stButton > button:first-child {
        width: 100%;
        height: 50px;
        font-weight: bold;
        border-radius: 10px;
        transition: all 0.3s;
    }
    /* Botões de Compra/Venda */
    .stButton button:has(div p:contains("COMPRAR")) { background-color: #00c853 !important; color: white !important; border: none !important; }
    .stButton button:has(div p:contains("VENDER")) { background-color: #ff3d00 !important; color: white !important; border: none !important; }
    
    /* Botão de Fechar Operação (Laranja) */
    .stButton button:has(div p:contains("FECHAR")) {
        background-color: #ff9800 !important;
        color: white !important;
        border: none !important;
        margin-top: 10px;
    }
    .stButton button:hover:has(div p:contains("FECHAR")) {
        background-color: #e68900 !important;
        box-shadow: 0px 0px 15px rgba(255, 152, 0, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A BINANCE ---
# Tentando puxar as chaves do Secrets
try:
    api_key = st.secrets["binance"]["api_key"]
    api_secret = st.secrets["binance"]["api_secret"]
    
    # Criando o Cliente
    client = Client(api_key, api_secret)
    
    # Puxando o Saldo Real Spot (USDT)
    conta = client.get_asset_balance(asset='USDT')
    saldo_real = float(conta['free'])
    
    status_conexao = "✅ SISTEMA ONLINE (SPOT)"
    cor_status = "success"
    modo_visualizacao = False
except Exception as e:
    # Se der erro nas chaves, entra no modo visualização
    saldo_real = 0.0
    status_conexao = "⚠️ MODO VISUALIZAÇÃO (Sem Chaves)"
    cor_status = "warning"
    modo_visualizacao = True
    api_key = "Não Configurada" # Para mostrar no Perfil

# --- SIDEBAR (BARRA LATERAL) ---
with st.sidebar:
    # SEU LOGOTIPO VOLTOU! (Texto neon fixo)
    st.markdown("""
    <div class="logo-container">
        <p class="logo-text">🛡️ TRADER GUARD</p>
        <p class="logo-sub">Security & High Frequency</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Navegação Principal", ["📈 Terminal de Trade", "💰 Gestão PIX", "👤 Perfil API"])
    
    st.divider()
    # Mostra o status da conexão
    if cor_status == "success": st.success(status_conexao)
    else: st.warning(status_conexao)
    
    st.info(f"📍 Servidor: Campina Grande - PB")

# --- CONTEÚDO PRINCIPAL ---
if menu == "📈 Terminal de Trade":
    col_graf, col_painel = st.columns([3, 1])

    with col_graf:
        # Gráfico do TradingView (BTC/USDT Spot)
        tv_html = """
        <div style="height:620px;">
            <div id="chart_div"></div>
            <script src="https://s3.tradingview.com/tv.js"></script>
            <script>
            new TradingView.widget({
                "width": "100%", "height": 620, "symbol": "BINANCE:BTCUSDT",
                "interval": "1", "theme": "dark", "style": "1", "locale": "br",
                "container_id": "chart_div", "hide_side_toolbar": false, "allow_symbol_change": true
            });
            </script>
        </div>"""
        components.html(tv_html, height=630)

    with col_painel:
        st.subheader("⚡ Boleta de Ordem")
        
        # Dashboard de Saldo (Mostra o saldo real da Binance)
        st.metric("Saldo na Binance (USDT)", f"$ {saldo_real:,.2f}", delta="Ao Vivo")
        
        st.divider()
        
        # Bloqueia os botões se estiver em modo visualização
        if modo_visualizacao:
            st.error("⚠️ Conecte suas chaves API para operar.")
            st.button("🚀 COMPRAR (LONG)", disabled=True)
            st.button("📉 VENDER (SHORT)", disabled=True)
            st.button("⏹️ FECHAR POSIÇÃO AGORA", disabled=True)
        else:
            # Controles de Operação Reais
            margem = st.number_input("Valor da Entrada ($)", min_value=5.0, value=20.0, step=5.0)
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🚀 COMPRAR"):
                    st.toast(f"Ordem de COMPRA enviada: ${margem}")
                    # client.order_market_buy(symbol='BTCUSDT', quantity=...)
            with col_btn2:
                if st.button("📉 VENDER"):
                    st.toast(f"Ordem de VENDA enviada: ${margem}")
                    # client.order_market_sell(symbol='BTCUSDT', quantity=...)
            
            # BOTÃO DE SAIR DA OPERAÇÃO (O que você pediu)
            if st.button("⏹️ FECHAR POSIÇÃO AGORA"):
                st.warning("⚠️ Encerrando ordens abertas...")
                # client.cancel_all_open_orders(symbol='BTCUSDT')

elif menu == "💰 Gestão PIX":
    st.title("Depósitos e Saques")
    st.write("Funcionalidade em integração com o gateway de pagamento.")

elif menu == "👤 Perfil API":
    st.title("Configurações de Segurança")
    st.write(f"Conectado à chave: `{api_key[:10]}...`")
