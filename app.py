# ================= IMPORTS =================
import streamlit as st
from binance.client import Client
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import hashlib
import time
import streamlit.components.v1 as components

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Trader Guard Profissional", layout="wide")

# ================= CONEXÃO SEGURA COM BINANCE =================
# Puxa direto do "Secrets" do Streamlit para evitar erros e vazamentos
try:
    api_key = st.secrets["BINANCE_KEY"]
    api_secret = st.secrets["BINANCE_SECRET"]
    # O tld='com' e o requests_params ajudam a evitar o erro de sincronização (Timestamp)
    client = Client(api_key, api_secret, tld='com', requests_params={'timeout': 20})
except Exception as e:
    st.error(f"Erro nas chaves do Secrets: {e}")
    client = None

# Configurações do Telegram (Opcional - deixe vazio no Secrets se não usar)
TOKEN = st.secrets.get("TELEGRAM_TOKEN", "")
CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID", "")

# ================= FUNÇÕES DE APOIO =================

def enviar_telegram(mensagem):
    if not TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem}, timeout=5)
    except: pass

def falar(texto):
    """Faz o navegador falar usando JavaScript (O Monstro agora tem voz!)"""
    componente_voz = f"""
        <script>
            var msg = new SpeechSynthesisUtterance('{texto}');
            msg.lang = 'pt-BR';
            window.speechSynthesis.speak(msg);
        </script>
    """
    components.html(componente_voz, height=0)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# ================= ESTADO DA SESSÃO =================
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'sinais_enviados' not in st.session_state: st.session_state['sinais_enviados'] = []

# ================= INDICADORES =================
intervalos = ["15m", "30m", "1h"]
pares = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT"]

def ema(series, period=200):
    return series.ewm(span=period, adjust=False).mean()

def get_candles(symbol, interval):
    if not client: return None
    try:
        # recv_window evita o erro de 'Timestamp for this request is outside of the recvWindow'
        klines = client.get_klines(symbol=symbol, interval=interval, limit=100, recv_window=60000)
        df = pd.DataFrame(klines, columns=["open_time","open","high","low","close","volume","close_time","qav","trades","tb_base","tb_quote","ignore"])
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df
    except: return None

# ================= LÓGICA DE ESTRATÉGIA =================
def checklist(df, symbol):
    df["EMA200"] = ema(df["close"])
    ultimo = df.iloc[-1]
    fundo = df["low"].iloc[-15:-1].min()
    
    # Estratégia Pullback (Simplificada para estabilidade)
    if ultimo["close"] > ultimo["EMA200"] and ultimo["low"] <= ultimo["EMA200"] and ultimo["close"] > ultimo["open"]:
        return {"par": symbol, "direcao": "COMPRA", "prob": 96}
    
    # Armadilha de Fundo
    if ultimo["low"] < fundo and ultimo["close"] > fundo and ultimo["close"] > ultimo["EMA200"]:
        return {"par": symbol, "direcao": "COMPRA", "prob": 95}
        
    return None

# ================= INTERFACE =================
st.title("🛡️ Trader Guard - Painel de Sinais")

if not st.session_state['logado']:
    st.sidebar.subheader("Acesso Restrito")
    u = st.sidebar.text_input("Usuário")
    p = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if u == "admin" and p == "admin": # Altere aqui sua senha
            st.session_state['logado'] = True
            st.rerun()
        else: st.sidebar.error("Incorreto")
else:
    col_monitor, col_grafico = st.columns([1, 3])

    with col_monitor:
        st.header("🚦 Radar")
        robo_ligado = st.toggle("🤖 Ativar Monitoramento")
        if st.button("Sair"): 
            st.session_state['logado'] = False
            st.rerun()
        
        # Botão para o navegador autorizar a voz
        if st.button("Ativar Voz do Monstro 🔊"):
            falar("Sistema de voz ativado com sucesso!")

    with col_grafico:
        par_v = st.selectbox("Moeda no Gráfico", pares)
        tv_html = f"""
            <div style="height:500px;">
                <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                <script type="text/javascript">
                new TradingView.widget({{"width": "100%", "height": 500, "symbol": "BINANCE:{par_v}", "interval": "15", "theme": "dark", "locale": "br", "container_id": "tv-chart"}});
                </script>
                <div id="tv-chart"></div>
            </div>
        """
        components.html(tv_html, height=510)

    # LOOP DE EXECUÇÃO
    if robo_ligado:
        st.toast("Buscando sinais...")
        for par in pares:
            for tempo in intervalos:
                df = get_candles(par, tempo)
                if df is not None:
                    sinal = checklist(df, par)
                    if sinal:
                        id_sinal = f"{par}_{tempo}_{sinal['direcao']}_{datetime.now().hour}"
                        if id_sinal not in st.session_state['sinais_enviados']:
                            st.session_state['sinais_enviados'].append(id_sinal)
                            falar(f"Atenção! Sinal de {sinal['direcao']} em {par}")
                            enviar_telegram(f"🚀 SINAL: {sinal['direcao']} em {par} ({tempo})")
                            st.sidebar.success(f"🔥 {par}: {sinal['direcao']} ({tempo})")

        time.sleep(60) # Espera 1 minuto para a próxima busca
        st.rerun()
