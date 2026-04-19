# --- CONEXÃO COM A BINANCE (VERSÃO FINAL DE TESTE) ---
import time

try:
    api_key = st.secrets["binance"]["api_key"]
    api_secret = st.secrets["binance"]["api_secret"]
    
    # Inicializa o cliente
    client = Client(api_key, api_secret)
    
    # FORÇA SINCRONIZAÇÃO DE HORÁRIO (Resolve erro de conexão no Streamlit Cloud)
    server_time = client.get_server_time()
    client.timestamp_offset = server_time['serverTime'] - int(time.time() * 1000)
    
    # Busca o saldo de forma mais segura
    info = client.futures_account_balance()
    
    # Tenta encontrar o USDT, se não achar, define como 0.0 em vez de travar
    saldo_real = 0.0
    for item in info:
        if item['asset'] == 'USDT':
            saldo_real = float(item['balance'])
            break
            
    status_conexao = "✅ SISTEMA ONLINE"

except Exception as e:
    saldo_real = 0.0
    # ISSO VAI ESCREVER O ERRO REAL NA BARRA LATERAL
    status_conexao = f"❌ ERRO: {str(e)}"
