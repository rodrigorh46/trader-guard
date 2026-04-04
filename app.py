# ================= IMPORTS =================
import streamlit as st
from binance.client import Client
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import hashlib
import time
import streamlit.components.v1 as components

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(page_title="Trader Guard Profissional", layout="wide")

# ================= API & TELEGRAM =================
try:
    # Puxa das configurações seguras do Streamlit (Secrets)
    api_key = st.secrets["BINANCE_KEY"]
    api_secret = st.secrets["BINANCE_SECRET"]
    # tld='com' ajuda a evitar bloqueios de região na nuvem
    client = Client(api_key, api_secret, tld='com')
except Exception as e:
    st.error(f"Erro de Configuração: {e}")
    client = None

TOKEN = st.secrets.get("TELEGRAM_TOKEN", "")
CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID", "")

def enviar_telegram(mensagem):
    if not TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem}, timeout=5)
    except: pass

def falar(texto):
    """RESOLUÇÃO DA VOZ: O Monstro fala no seu Navegador/Celular"""
    componente_voz = f"""
        <script>
            var msg = new SpeechSynthesisUtterance('{texto}');
            msg.lang = 'pt-BR';
            window.speechSynthesis.speak(msg);
        </script>
    """
    components.html(componente_voz, height=0)

# ================= ESTADO DA SESSÃO =================
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

if 'usuarios_db' not in st.session_state:
    st.session_state['usuarios_db'] = {"admin": hash_senha("admin")} 
if 'logado' not in st.session_state:
    st.session_state['logado'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = ""
if 'sinais_enviados' not in st.session_state:
    st.session_state['sinais_enviados'] = [] 

def autenticar(usuario, senha):
    return st.session_state['usuarios_db'].get(usuario) == hash_senha(senha)

# ================= INDICADORES & DADOS =================
intervalos = ["15m", "30m", "1h"] 
pares = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT"]

def ema(series, period=200):
    return series.ewm(span=period, adjust=False).mean()

def atr(df, period=14):
    high_low = df["high"] - df["low"]
    high_close = abs(df["high"] - df["close"].shift())
    low_close = abs(df["low"] - df["close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def get_candles(symbol, interval, limit=100):
    if not client: return None
    try:
        # recv_window=60000 resolve erros de fuso horário com a Binance
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit, recv_window=60000)
        df = pd.DataFrame(klines, columns=["open_time","open","high","low","close","volume","close_time","qav","trades","tb_base","tb_quote","ignore"])
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)
        return df
    except: return None

# ================= LÓGICA DE SINAIS (MANTIDA) =================
def checklist(df, symbol):
    df["EMA200"] = ema(df["close"])
    df["ATR"] = atr(df)
    ultimo = df.iloc[-1]
    media_vol = df["volume"].rolling(20).mean().iloc[-1]
    topo = df["high"].iloc[-10:-1].max()
    fundo = df["low"].iloc[-10:-1].min()

    if df["ATR"].iloc[-1] < df["ATR"].mean() * 0.5:
        return None

    # Pullback Perfeito 96%
    if ultimo["close"] > ultimo["EMA200"] and ultimo["low"] <= ultimo["EMA200"] and ultimo["close"] > ultimo["open"]:
        return {"par": symbol, "direcao": "COMPRA", "prob": 96, "risco": "MUITO BAIXO"}

    # Armadilhas 95%
    if ultimo["low"] < fundo and ultimo["close"] > fundo and ultimo["volume"] > media_vol*1.5 and ultimo["close"] > ultimo["EMA200"]:
        return {"par": symbol, "direcao":"COMPRA", "prob":95, "risco":"BAIXO"}
    if ultimo["high"] > topo and ultimo["close"] < topo and ultimo["volume"] > media_vol*1.5 and ultimo["close"] < ultimo["EMA200"]:
        return {"par": symbol, "direcao":"VENDA", "prob":95, "risco":"BAIXO"}

    return None

# ================= ALERTA DE PROXIMIDADE (MANTIDO) =================
def alerta_proximidade(df, symbol, tempo):
    ultimo = df.iloc[-1]
    EMA = ema(df["close"]).iloc[-1]
    margem = EMA * 0.005 
    if EMA - margem <= ultimo["close"] <= EMA + margem:
        id_prox = f"prox_{symbol}_{tempo}_{datetime.now().minute}"
        if id_prox not in st.session_state['sinais_enviados']:
            st.session_state['sinais_enviados'].append(id_prox)
            falar(f"Atenção. {symbol} próximo da média de 200.")
            st.sidebar.warning(f"⚠️ {symbol} ({tempo}) Perto da EMA200")

def processar_alerta(sinal, tempo):
    id_sinal = f"{sinal['par']}_{tempo}_{sinal['direcao']}_{datetime.now().strftime('%H:%M')}"
    if id_sinal not in st.session_state['sinais_enviados']:
        st.session_state['sinais_enviados'].append(id_sinal)
        emoji = "🟢 COMPRA" if sinal['direcao'] == "COMPRA" else "🔴 VENDA"
        msg_tg = f"{emoji} SINAL VALIDADO\n🪙 {sinal['par']} ({tempo})\n🎯 Prob: {sinal['prob']}%\n⚠️ Risco: {sinal['risco']}"
        enviar_telegram(msg_tg)
        falar(f"Sinal de {sinal['direcao']} em {sinal['par']} no tempo {tempo}.")
        return True
    return False

# ================= INTERFACE PRINCIPAL =================
st.title("🛡️ Trader Guard - Campina Grande")

if not st.session_state['logado']:
    st.sidebar.subheader("🔐 Login")
    u_input = st.sidebar.text_input("Usuário")
    p_input = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if autenticar(u_input, p_input):
            st.session_state['logado'] = True
            st.rerun()
        else: st.sidebar.error("Dados incorretos.")
else:
    st.sidebar.success(f"👤 Trader: {st.session_state['usuario']}")
    if st.sidebar.button("Ativar Voz do Monstro 🔊"): falar("Voz ativada com sucesso!")
    if st.sidebar.button("Sair"):
        st.session_state['logado'] = False
        st.rerun()

    col_monitor, col_grafico = st.columns([1, 3])
    with col_monitor:
        st.header("🚦 Radar")
        robo_ligado = st.toggle("🤖 Ligar Robô")
        placeholder_alertas = st.container()

    with col_grafico:
        par_v = st.selectbox("Par Visual", pares)
        tempo_v = st.selectbox("Intervalo", ["1", "5", "15", "60", "240"], index=2)
        tv_html = f'<div style="height:650px;"><script src="https://s3.tradingview.com/tv.js"></script><script>new TradingView.widget({{"autosize": true, "symbol": "BINANCE:{par_v}", "interval": "{tempo_v}", "timezone": "America/Sao_Paulo", "theme": "dark", "style": "1", "locale": "br", "container_id": "tv-chart"}});</script><div id="tv-chart"></div></div>'
        components.html(tv_html, height=660)

    if robo_ligado:
        for par in pares:
            for tempo in intervalos:
                df = get_candles(par, tempo)
                if df is not None:
                    # Lógica de Alerta de Proximidade
                    alerta_proximidade(df, par, tempo)
                    
                    sinal = checklist(df, par)
                    if sinal:
                        # Trava de Divergência do BTC
                        df_btc = get_candles("BTCUSDT", tempo)
                        if df_btc is not None:
                            ema_btc = ema(df_btc["close"]).iloc[-1]
                            preco_btc = df_btc["close"].iloc[-1]
                            if (sinal["direcao"] == "COMPRA" and preco_btc < ema_btc) or \
                               (sinal["direcao"] == "VENDA" and preco_btc > ema_btc):
                                sinal = None
                        
                        if sinal:
                            processar_alerta(sinal, tempo)
                            with placeholder_alertas:
                                cor = "green" if sinal['direcao'] == "COMPRA" else "red"
                                st.markdown(f"**{par} ({tempo})**: :{cor}[{sinal['direcao']}]")
        
        time.sleep(30)
        st.rerun()
