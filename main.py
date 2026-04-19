import streamlit as st
from binance.client import Client
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard PRO", layout="wide")

# --- CONEXÃO COM A BINANCE ---
try:
    api_key = st.secrets["binance"]["api_key"]
    api_secret = st.secrets["binance"]["api_secret"]
    
    # Inicializa o cliente (Corrigido para 'client' minúsculo)
    client = Client(api_key, api_secret)
    
    # FORÇA SINCRONIZAÇÃO DE HORÁRIO
    server_time = client.get_server_time()
    client.timestamp_offset = server_time['serverTime'] - int(time.time() * 1000)
    
    # Busca o saldo de Futuros
    info = client.futures_account_balance()
    saldo_real = 0.0
    for item in info:
        if item['asset'] == 'USDT':
            saldo_real = float(item['balance'])
            break
            
    status_conexao = "✅ SISTEMA ONLINE"

except Exception as e:
    saldo_real = 0.0
    # Isso vai mostrar o erro real na barra lateral se algo falhar
    status_conexao = f"❌ ERRO: {str(e)}"

# --- INTERFACE (O ESTILO VÍRUS) ---
st.sidebar.markdown("### ⚡ TRADER GUARD PRO")
st.sidebar.metric("Saldo Atual (USDT)", f"$ {saldo_real:,.2f}")
st.sidebar.info(status_conexao)

# Seletor de Moeda
par = st.selectbox("Selecione o Alvo", ["BTCUSDT", "SOLUSDT", "ETHUSDT", "XRPUSDT"])

# Gráfico do TradingView
st.components.v1.html(f"""
    <div id="tradingview_chart" style="height:500px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "autosize": true, "symbol": "BINANCE:{par}", "interval": "15",
      "theme": "dark", "style": "1", "locale": "br", "container_id": "tradingview_chart"
    }});
    </script>
""", height=500)

# Botões de Operação
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 EXECUTAR COMPRA", use_container_width=True):
        st.write(f"Ordem de Compra enviada para {par}")
with col2:
    if st.button("📉 EXECUTAR VENDA", use_container_width=True):
        st.write(f"Ordem de Venda enviada para {par}")
