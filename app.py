import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'vizinhança_cuidadora_key_2026'

# --- CONFIGURAÇÕES ---
UPLOAD_FOLDER = 'certificados'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def conectar_bd():
    conn = sqlite3.connect('vizinhanca.db')
    conn.row_factory = sqlite3.Row 
    return conn

def configurar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profissionais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            especialidade TEXT NOT NULL,
            valor_servico REAL NOT NULL,
            localidade TEXT NOT NULL,
            stellar_pubkey TEXT,
            validado INTEGER DEFAULT 0,
            certificado_path TEXT
        )
    """)
    conn.commit()
    conn.close()

configurar_tabela()

# --- ROTAS ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# ESTA É A ROTA QUE RECEBE OS DADOS DO FORMULÁRIO
@app.route('/enviar_cadastro', methods=['POST'])
def enviar_cadastro():
    nome = request.form.get('nome')
    especialidade = request.form.get('especialidade')
    localidade = request.form.get('localidade')
    
    # Ajuste para pegar o campo correto do seu HTML
    valor_str = request.form.get('valor') or "0"
    valor = float(valor_str.replace(',', '.'))

    # O campo no seu HTML de cadastro se chama 'doc', não 'certificado'
    arquivo = request.files.get('doc')
    caminho_certificado = ""
    if arquivo and arquivo.filename != '':
        nome_arquivo = secure_filename(f"{nome}_{arquivo.filename}")
        caminho_certificado = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        arquivo.save(caminho_certificado)

    try:
        with conectar_bd() as conexao:
            cursor = conexao.cursor()
            # Salva com validado = 0 para aparecer na curadoria
            cursor.execute("""
                INSERT INTO profissionais (nome, especialidade, valor_servico, localidade, validado, certificado_path)
                VALUES (?, ?, ?, ?, 0, ?)
            """, (nome, especialidade, valor, localidade, caminho_certificado))
            conexao.commit()
        
        flash("Cadastro enviado com sucesso!", "success")
        return redirect(url_for('home')) # Ou uma página de sucesso
    except Exception as e:
        flash(f"Erro ao cadastrar: {str(e)}", "danger")
        return redirect(url_for('cadastro'))

@app.route('/admin')
def admin_geral():
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        # Pega quem tem validado = 0 (Pendente)
        cursor.execute("SELECT * FROM profissionais WHERE validado = 0")
        pendentes = cursor.fetchall()
        
        # Agendamentos fictícios para não quebrar o dashboard
        agendamentos_ficticios = [
            {'iniciais': 'MA', 'paciente': 'Maria Andrade', 'endereco': 'Rua Flores, 123', 'horario': '09:00'},
            {'iniciais': 'JS', 'paciente': 'João Silva', 'endereco': 'Av. Central, 450', 'horario': '14:30'}
        ]

    return render_template('admin.html', 
                           profissionais=pendentes, 
                           agendamentos=agendamentos_ficticios)

@app.route('/validar/<int:id>')
def validar_profissional(id):
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute("UPDATE profissionais SET validado = 1 WHERE id = ?", (id,))
        conexao.commit()
    flash("Profissional aprovado!", "success")
    return redirect(url_for('admin_geral'))

@app.route('/criar_carteira/<int:id>')
def criar_carteira(id):
    chave_fake = f"GB{id}STELLAR_FAKE_KEY"
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute("UPDATE profissionais SET stellar_pubkey = ? WHERE id = ?", (chave_fake, id))
        conexao.commit()
    flash("Carteira ativada!", "success")
    return redirect(url_for('admin_geral'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)