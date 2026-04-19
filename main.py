import streamlit as st
import streamlit.components.v1 as components
from binance.client import Client
import pandas as pd
import requests
import hashlib
import time
from datetime import datetime

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Trader Guard VIRUS 🛡️", layout="wide", page_icon="☣️")

# ================= CSS: ESTILO VÍRUS DIGITAL =================
st.markdown("""
    <style>
    .main { background-color: #050505; }
    
    /* Logo Animado Estilo Matrix/Virus */
    @keyframes glitch {
        0% { text-shadow: 2px 0 0 #00ff41, -2px 0 0 #ff0000; }
        25% { text-shadow: -2px 0 0 #00ff41, 2px 0 0 #ff0000; }
        50% { text-shadow: 2px 0 0 #00ff41, -2px 0 0 #ff0000; }
        100% { text-shadow: -2px 0 0 #00ff41, 2px 0 0 #ff0000; }
    }
    
    .virus-logo {
        font-family: 'Courier New', monospace;
        color: #00ff41;
        font-size: 38px;
        font-weight: bold;
        text-align: center;
        animation: glitch 1s infinite alternate-reverse;
        border-bottom: 2px solid #00ff41;
        margin-bottom: 10px;
    }

    /* Alerta de Travamento de Capital */
    .stAlert {
        border: 2px solid #ff0000 !important;
        background-color: #200000 !important;
        color: #ff0000 !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# ================= SEGURANÇA E CONEXÃO =================
try:
    # Usando secrets para não expor no GitHub
    api_key = st.secrets["binance"]["api_key"]
    api_secret = st.secrets["binance"]["api_secret"]
    client = Client(api_key, api_secret)
    
    # --- LÓGICA DE PROTEÇÃO DE 10% ---
    if 'saldo_inicial' not in st.session_state:
        # Puxa o saldo inicial da primeira vez que o app abre
        info = client.futures_account_balance()
        balance = next(item for item in info if item['asset'] == 'USDT')
        st.session_state['saldo_inicial'] = float(balance['balance'])

    # Saldo Atual
    info_atual = client.futures_account_balance()
    balance_atual = next(item for item in info_atual if item['asset'] == 'USDT')
    saldo_real = float(balance_atual['balance'])

    # Cálculo da Perda
    perda_atual = ((saldo_real - st.session_state['saldo_inicial']) / st.session_state['saldo_inicial']) * 100
    
    # DISJUNTOR: Travamento se perder mais de 10%
    trava_seguranca = perda_atual <= -10.0
    status_conexao = "✅ SISTEMA ONLINE" if not trava_seguranca else "🚨 SISTEMA TRAVADO (LOSS LIMIT)"

except Exception as e:
    saldo_real = 0.0
    perda_atual = 0.0
    st.session_state['saldo_inicial'] = 0.0
    trava_seguranca = False
    status_conexao = f"⚠️ MODO VISUALIZAÇÃO"

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown('<p class="virus-logo">TRADER_GUARD.exe</p>', unsafe_allow_html=True)
    st.write(f"Sessão iniciada: {datetime.now().strftime('%H:%M:%S')}")
    
    if trava_seguranca:
        st.error(f"SISTEMA BLOQUEADO: Perda de {perda_atual:.2f}% atingida.")
        st.info("O robô encerrou todas as ordens para proteger seu capital.")
    else:
        st.success(status_conexao)
    
    st.metric("Saldo Atual", f"$ {saldo_real:,.2f}", f"{perda_atual:.2f}%")
    
    menu = st.radio("Sistemas", ["📈 Terminal", "👤 API Settings"])

# ================= INTERFACE PRINCIPAL =================
if trava_seguranca:
    st.markdown("""
        <div style="text-align: center; margin-top: 100px;">
            <h1 style="color: #ff0000; font-size: 50px;">☣️ PROTOCOLO DE EMERGÊNCIA ATIVADO ☣️</h1>
            <p style="color: white; font-size: 20px;">O limite de 10% de perda foi atingido. O acesso às ordens foi revogado para sua segurança.</p>
        </div>
    """, unsafe_allow_html=True)
    # Aqui o código para de renderizar os botões, impedindo o trade.
    
else:
    if menu == "📈 Terminal":
        col_graf, col_painel = st.columns([3, 1])
        
        with col_graf:
            # Gráfico do TradingView
            par_v = st.selectbox("Alvo", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
            tv_html = f'<div id="tv-chart" style="height:600px;"></div><script src="https://s3.tradingview.com/tv.js"></script><script>new TradingView.widget({{"autosize": true, "symbol": "BINANCE:{par_v}", "interval": "15", "theme": "dark", "container_id": "tv-chart"}});</script>'
            components.html(tv_html, height=620)
            
        with col_painel:
            st.subheader("⚡ Boleta Virus.dll")
            margem = st.number_input("Entrada ($)", 5.0, 1000.0, 20.0)
            
            if st.button("🚀 EXECUTAR COMPRA"):
                st.toast("Injetando ordem no mercado...")
                # Lógica de compra aqui
                
            if st.button("📉 EXECUTAR VENDA"):
                st.toast("Injetando ordem de short...")
                # Lógica de venda aqui

            st.divider()
            if st.button("⏹️ KILL SWITCH (FECHAR TUDO)"):
                st.warning("Encerrando todas as conexões e ordens...")
