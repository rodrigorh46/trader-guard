import streamlit as st
import streamlit.components.v1 as components

# 1. Configuração da Página
st.set_page_config(page_title="Trader Guard HFT", layout="wide")

# 2. CSS DEFINITIVO (Forçando cores pelo texto do botão)
st.markdown("""
    <style>
    /* Fundo do App */
    .stApp { background-color: #0e1117; color: white; }
    
    /* Cor do Botão COMPRAR */
    button:has(div p:contains("COMPRAR")) {
        background-color: #00c087 !important;
        color: white !important;
        border: none !important;
        height: 3.5em !important;
        width: 100% !important;
    }
    
    /* Cor do Botão VENDEDOR */
    button:has(div p:contains("VENDEDOR")) {
        background-color: #ff3b69 !important;
        color: white !important;
        border: none !important;
        height: 3.5em !important;
        width: 100% !important;
    }

    /* Ajuste da Sidebar */
    [data-testid="stSidebar"] { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# 3. Dicionário de Ativos (Futuros)
ativos = {
    "BTC/USDT (Futuros)": "BINANCE:BTCUSDT.P",
    "ETH/USDT (Futuros)": "BINANCE:ETHUSDT.P",
    "SOL/USDT (Futuros)": "BINANCE:SOLUSDT.P",
    "XRP/USDT (Futuros)": "BINANCE:XRPUSDT.P"
}

# 4. Navegação Lateral (TODOS OS MENUS ESTÃO AQUI)
with st.sidebar:
    st.title("🛡️ Trader Guard")
    # Este é o menu que controla o que aparece na tela
    menu = st.radio("Navegação", ["📈 Operacional", "💰 Depósito PIX", "💸 Saque PIX", "👤 Minha Conta"])
    
    st.divider()
    if menu == "📈 Operacional":
        escolha = st.selectbox("Selecione o Ativo", list(ativos.keys()))
        simbolo_ativo = ativos[escolha]
    st.caption("🛡️ Trava de Segurança 10% Ativa")

# 5. Lógica das Telas (O que aparece quando você clica)
if menu == "📈 Operacional":
    st.subheader(f"Painel HFT: {escolha}")
    col_graf, col_painel = st.columns([3, 1])

    with col_graf:
        # Gráfico Dinâmico
        tv_html = f"""
        <div style="height:600px;">
            <div id="chart_div"></div>
            <script src="https://s3.tradingview.com/tv.js"></script>
            <script>
            new TradingView.widget({{
                "width": "100%", "height": 600, "symbol": "{simbolo_ativo}",
                "interval": "15", "theme": "dark", "style": "1", "locale": "br",
                "container_id": "chart_div"
            }});
            </script>
        </div>"""
        components.html(tv_html, height=610)

    with col_painel:
        st.write("### Execução")
        st.metric("Saldo Disponível", "R$ 1.000,00")
        st.divider()
        margem = st.number_input("Margem (R$)", 10.0, 5000.0, 100.0)
        alav = st.slider("Alavancagem", 1, 20, 10)
        
        # Botões que usam o CSS acima
        if st.button("COMPRAR (LONG)"):
            st.success("Ordem enviada!")
        if st.button("VENDEDOR (CURTO)"):
            st.error("Ordem enviada!")

elif menu == "💰 Depósito PIX":
    st.title("Depósito Instantâneo")
    st.write("Transfira para sua conta agora.")
    v_dep = st.number_input("Valor", 20.0)
    if st.button("Gerar QR Code"):
        st.code("CHAVE_PIX_EXEMPLO_COPIA_E_COLA")
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=TraderGuard")

elif menu == "💸 Saque PIX":
    st.title("Retirada de Lucro")
    st.number_input("Valor do Saque", 10.0)
    st.text_input("Sua Chave PIX")
    st.button("Confirmar Saque")

elif menu == "👤 Minha Conta":
    st.title("Perfil de Usuário")
    aba1, aba2 = st.tabs(["Acessar", "Cadastrar"])
    with aba1:
        st.text_input("E-mail")
        st.text_input("Senha", type="password")
        st.button("Entrar")
    with aba2:
        st.text_input("Nome")
        st.text_input("E-mail Novo")
        st.button("Criar Conta")
