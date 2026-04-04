import streamlit as st
import pandas as pd
from binance.client import Client
import time

# --- CONFIGURAÇÃO DAS CHAVES (PEGA DO SECRETS) ---
api_key = st.secrets["BINANCE_KEY"]
api_secret = st.secrets["BINANCE_SECRET"]
client = Client(api_key, api_secret)

# --- FUNÇÃO MÁGICA PARA O MONSTRO FALAR NO NAVEGADOR ---
def falar(texto):
    """Faz o navegador (Chrome/Safari) falar o sinal em português"""
    componente_voz = f"""
        <script>
            var msg = new SpeechSynthesisUtterance('{texto}');
            msg.lang = 'pt-BR';
            msg.rate = 1;
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(componente_voz, height=0)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Trader Guard - Sinais", layout="wide")
st.title("🛡️ Trader Guard - Monitoramento Real")

# --- GRÁFICO DO TRADINGVIEW ---
st.subheader("Gráfico em Tempo Real (Bitcoin)")
st.components.v1.html(
    """
    <div style="height:400px;">
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({
          "width": "100%",
          "height": 400,
          "symbol": "BINANCE:BTCUSDT",
          "interval": "1",
          "timezone": "America/Sao_Paulo",
          "theme": "dark",
          "style": "1",
          "locale": "br",
          "toolbar_bg": "#f1f3f6",
          "enable_publishing": false,
          "allow_symbol_change": true,
          "container_id": "tv_chart"
        });
        </script>
        <div id="tv_chart"></div>
    </div>
    """,
    height=400,
)

# --- LÓGICA DE MONITORAMENTO ---
st.write("---")
st.write("🛰️ Aguardando sinais de Pullback e Cruzamento...")

# Simulando a busca de preço e alerta
try:
    # Busca o preço atual apenas para mostrar que está conectado
    ticker = client.get_symbol_ticker(symbol="BTCUSDT")
    preco_atual = float(ticker['price'])
    st.metric("Preço Atual Bitcoin (BTC/USDT)", f"US$ {preco_atual:,.2f}")

    # Exemplo de Alerta (O Monstro fala aqui)
    # Se bater sua estratégia, o comando abaixo faz o som:
    if st.button("Teste a Voz do Monstro 🔊"):
        falar("Atenção Rodrigo! O Trader Guard identificou uma oportunidade de lucro!")

except Exception as e:
    st.error(f"Erro de conexão com a Binance: {e}")
    st.info("Verifique se as chaves no 'Secrets' estão corretas!")

# --- RODAPÉ ---
st.sidebar.info("Trader Guard v1.0 - Rodando na Nuvem")
