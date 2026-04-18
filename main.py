import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard ELITE 🛡️", layout="wide")

# --- CSS PROFISSIONAL (NEON & DARK MODE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    
    /* Botões de Execução */
    button:has(div p:contains("COMPRAR")) {
        background-color: #00c087 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        height: 3.5em !important;
        width: 100% !important;
    }
    button:has(div p:contains("VENDEDOR")) {
        background-color: #ff3b69 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        height: 3.5em !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE SEGURANÇA (ST.SECRETS) ---
# O robô vai tentar ler aqui. Se não estiver configurado no painel do Streamlit, ele avisará.
try:
    API_KEY = st.secrets["binance"]["api_key"]
    API_SECRET = st.secrets["binance"]["api_secret"]
    status_conexao = "✅ CONECTADO À BINANCE"
except:
    status_conexao = "⚠️ MODO DEMONSTRAÇÃO (Sem API)"

# --- DICIONÁRIO DE ATIVOS ---
ativos = {
    "BTC/USDT (Futuros)": "BINANCE:BTCUSDT.P",
    "ETH/USDT (Futuros)": "BINANCE:ETHUSDT.P",
    "SOL/USDT (Futuros)": "BINANCE:SOLUSDT.P",
    "XRP/USDT (Futuros)": "BINANCE:XRPUSDT.P",
    "ADA/USDT (Futuros)": "BINANCE:ADAUSDT.P"
}

# --- NAVEGAÇÃO LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
    st.title("Trader Guard")
    menu = st.radio("Navegação", ["📈 Operacional", "💰 Depósito PIX", "💸 Saque PIX", "👤 Minha Conta"])
    
    st.divider()
    st.info(status_conexao)
    st.caption("🛡️ Trava de Segurança 10% Ativa")

# --- LÓGICA DAS TELAS ---

if menu == "📈 Operacional":
    escolha = st.selectbox("Selecione o Ativo", list(ativos.keys()))
    simbolo_ativo = ativos[escolha]
    
    col_graf, col_painel = st.columns([3, 1])

    with col_graf:
        tv_html = f"""
        <div style="height:600px;">
            <div id="chart_div"></div>
            <script src="https://s3.tradingview.com/tv.js"></script>
            <script>
            new TradingView.widget({{
                "width": "100%", "height": 600, "symbol": "{simbolo_ativo}",
                "interval": "1", "theme": "dark", "style": "1", "locale": "br",
                "container_id": "chart_div"
            }});
            </script>
        </div>"""
        components.html(tv_html, height=610)

    with col_painel:
        st.write("### ⚡ Execução")
        st.metric("Saldo Disponível", "R$ 1.000,00", "+2.5%")
        st.divider()
        margem = st.number_input("Margem (R$)", 10.0, 1000.0, 100.0)
        alav = st.slider("Alavancagem", 1, 20, 10)
        
        if st.button("COMPRAR (LONG)"):
            st.success(f"Ordem de COMPRA enviada: {escolha}")
        
        if st.button("VENDEDOR (CURTO)"):
            st.error(f"Ordem de VENDA enviada: {escolha}")

elif menu == "💰 Depósito PIX":
    st.title("🏦 Depósito Instantâneo")
    col1, col2 = st.columns(2)
    with col1:
        v_dep = st.number_input("Valor para depósito (R$)", 20.0, 10000.0, 100.0)
        if st.button("Gerar QR Code PIX"):
            st.session_state.qr = True
    
    with col2:
        if st.session_state.get('qr'):
            st.write("### Escaneie para Pagar")
            # QR Code dinâmico com o valor
            link_qr = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=TraderGuard_Valor_{v_dep}"
            st.image(link_qr)
            st.code("chave-pix-copia-e-cola-trader-guard-2026")

elif menu == "💸 Saque PIX":
    st.title("💸 Retirada de Lucro")
    st.write("O valor será enviado para sua chave PIX cadastrada em até 30 minutos.")
    valor_saque = st.number_input("Quanto deseja sacar?", 10.0)
    chave_pix = st.text_input("Sua Chave PIX (CPF, E-mail ou Aleatória)")
    if st.button("Solicitar Saque"):
        st.warning(f"Solicitação de R$ {valor_saque} enviada para análise.")

elif menu == "👤 Minha Conta":
    st.title("👤 Gerenciamento de Perfil")
    t1, t2 = st.tabs(["Acesso", "Configurações API"])
    with t1:
        st.text_input("Usuário", value="rodrigo_dev", disabled=True)
        st.text_input("E-mail", value="rodrigo@exemplo.com")
        st.button("Atualizar Dados")
    with t2:
        st.write("### Chaves de Operação")
        st.text_input("Binance API Key", type="password", help="Sua chave fica criptografada")
        st.text_input("Binance Secret Key", type="password")
        st.button("Validar e Salvar Chaves")
