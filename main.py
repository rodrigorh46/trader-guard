import streamlit as st
import sqlite3, bcrypt, requests, time

# --- BANCO DE DADOS ---
conn = sqlite3.connect("usuarios.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    senha_hash TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)""")
conn.commit()

# --- FUNÇÕES DE USUÁRIO ---
def cadastrar_usuario(nome, email, senha):
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
                  (nome, email, senha_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_usuario(email, senha):
    c.execute("SELECT id, nome, senha_hash FROM usuarios WHERE email=?", (email,))
    user = c.fetchone()
    if user and bcrypt.checkpw(senha.encode('utf-8'), user[2]):
        return {"id": user[0], "nome": user[1], "email": email}
    return None

# --- FUNÇÕES PIX (OpenPix) ---
API_KEY = st.secrets["openpix"]["api_key"]

def gerar_qr_pix(valor):
    payload = {
        "value": int(valor * 100),
        "comment": "Depósito Trader Guard",
        "correlationID": f"TG-{int(time.time())}"
    }
    res = requests.post("https://api.openpix.com.br/api/v1/charge",
                        headers={"Authorization": API_KEY}, json=payload).json()
    return res["charge"]["qrCodeImage"], res["charge"]["paymentLink"]

def solicitar_saque(chave_pix, valor):
    payload = {
        "value": int(valor * 100),
        "comment": "Saque Trader Guard",
        "pixKey": chave_pix
    }
    res = requests.post("https://api.openpix.com.br/api/v1/pix",
                        headers={"Authorization": API_KEY}, json=payload).json()
    return res

# --- INTERFACE ---
st.set_page_config(page_title="Trader Guard", layout="wide")
st.title("🛡️ Trader Guard")

if "usuario" not in st.session_state:
    escolha = st.radio("Selecione:", ["Login", "Cadastro"])

    if escolha == "Cadastro":
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Cadastrar"):
            if cadastrar_usuario(nome, email, senha):
                st.success("✅ Usuário cadastrado com sucesso!")
            else:
                st.error("❌ Email já cadastrado.")

    elif escolha == "Login":
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            usuario = login_usuario(email, senha)
            if usuario:
                st.session_state["usuario"] = usuario
                st.success(f"Bem-vindo, {usuario['nome']}!")
            else:
                st.error("❌ Email ou senha inválidos.")
else:
    usuario = st.session_state["usuario"]
    st.sidebar.success(f"👤 Logado como {usuario['nome']}")
    menu = st.sidebar.radio("Navegação", ["🔴 Terminal", "💰 Depósito PIX", "💸 Saque PIX", "👤 Conta"])

    if menu == "💰 Depósito PIX":
        st.header("Depósito via PIX")
        valor_pix = st.number_input("Valor para Depósito (R$)", min_value=10.0, value=50.0)
        if st.button("Gerar Código PIX"):
            qr_url, link = gerar_qr_pix(valor_pix)
            st.image(qr_url)
            st.code(link, language="text")
            st.info("Use o QR ou link para pagar via PIX. O saldo será creditado após confirmação.")

    elif menu == "💸 Saque PIX":
        st.header("Saque via PIX")
        chave = st.text_input("Informe sua chave PIX")
        valor_saque = st.number_input("Valor para Saque (R$)", min_value=10.0, value=50.0)
        if st.button("Solicitar Saque"):
            resultado = solicitar_saque(chave, valor_saque)
            if "pix" in resultado:
                st.success("✅ Saque solicitado com sucesso!")
            else:
                st.error("❌ Erro ao solicitar saque.")

    elif menu == "👤 Conta":
        st.header("Minha Conta")
        st.write(f"Nome: {usuario['nome']}")
        st.write(f"Email: {usuario['email']}")
        if st.button("Logout"):
            del st.session_state["usuario"]
            st.info("Você saiu da conta.")
