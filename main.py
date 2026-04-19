import streamlit as st
import sqlite3, bcrypt, time, pandas as pd

# --- BANCO DE DADOS ---
conn = sqlite3.connect("usuarios.db", check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    senha_hash TEXT,
    saldo REAL DEFAULT 0
)""")
conn.commit()

# --- FUNÇÕES ---
def cadastrar_usuario(nome, email, senha):
    if not nome or not email or not senha:
        return False
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
                  (nome, email, senha_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_usuario(email, senha):
    c.execute("SELECT id, nome, senha_hash, saldo FROM usuarios WHERE email=?", (email,))
    user = c.fetchone()
    if user and bcrypt.checkpw(senha.encode('utf-8'), user[2]):
        return {"id": user[0], "nome": user[1], "email": email, "saldo": user[3]}
    return None

def atualizar_saldo(user_id, novo_saldo):
    c.execute("UPDATE usuarios SET saldo=? WHERE id=?", (novo_saldo, user_id))
    conn.commit()

# --- PIX FAKE ---
def gerar_qr_pix(valor):
    fake_qr = f"https://fake.qr/{valor}-{int(time.time())}"
    return fake_qr

# --- INTERFACE ---
st.set_page_config(page_title="Trader Guard", layout="wide")

with st.sidebar:
    st.markdown("🛡️ TRADER GUARD")

st.title("🛡️ Trader Guard")

if "usuario" not in st.session_state:
    escolha = st.radio("Selecione:", ["Login", "Cadastro"])
    if escolha == "Cadastro":
        nome = st.text_input("Nome completo")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Cadastrar"):
            if cadastrar_usuario(nome, email, senha):
                st.success("Cadastro realizado com sucesso! Faça login.")
            else:
                st.error("Erro: verifique os campos ou email já cadastrado.")
    else:
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Login"):
            user = login_usuario(email, senha)
            if user:
                st.session_state["usuario"] = user
                st.success(f"Bem-vindo, {user['nome']}!")
            else:
                st.error("Credenciais inválidas.")
else:
    usuario = st.session_state["usuario"]
    st.sidebar.success(f"👤 Logado como {usuario['nome']}")
    menu = st.sidebar.radio("Navegação", ["🔴 Terminal", "💰 Depósito PIX", "💸 Saque PIX", "👤 Conta"])

    if menu == "🔴 Terminal":
        st.subheader("📈 Gráfico simples do saldo")
        dados = pd.DataFrame({"Saldo":[usuario["saldo"]]}, index=[pd.Timestamp.now()])
        st.line_chart(dados)

    elif menu == "💰 Depósito PIX":
        valor_pix = st.number_input("Valor para Depósito (R$)", min_value=10.0, value=50.0)
        if st.button("Gerar Código PIX"):
            qr_url = gerar_qr_pix(valor_pix)
            st.code(qr_url, language="text")
            novo_saldo = usuario["saldo"] + valor_pix
            atualizar_saldo(usuario["id"], novo_saldo)
            usuario["saldo"] = novo_saldo
            st.success(f"Saldo atualizado: R$ {novo_saldo:.2f}")

    elif menu == "💸 Saque PIX":
        valor_saque = st.number_input("Valor para Saque (R$)", min_value=10.0, value=50.0)
        if st.button("Solicitar Saque"):
            if valor_saque <= usuario["saldo"]:
                novo_saldo = usuario["saldo"] - valor_saque
                atualizar_saldo(usuario["id"], novo_saldo)
                usuario["saldo"] = novo_saldo
                st.success(f"Saque realizado. Saldo atual: R$ {novo_saldo:.2f}")
            else:
                st.error("❌ Saldo insuficiente.")

    elif menu == "👤 Conta":
        st.write(f"Nome: {usuario['nome']}")
        st.write(f"Email: {usuario['email']}")
        st.write(f"Saldo atual: R$ {usuario['saldo']:.2f}")
        if st.button("Logout"):
            del st.session_state["usuario"]
            st.info("Você saiu da conta.")
