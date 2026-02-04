import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'vizinhança_cuidadora_key_2026'

# --- CONFIGURAÇÕES ---
UPLOAD_FOLDER = 'static/certificados'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def conectar_bd():
    conn = sqlite3.connect('vizinhanca.db')
    conn.row_factory = sqlite3.Row 
    return conn

def configurar_tabela():
    with conectar_bd() as conn:
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

configurar_tabela()

# --- ROTAS ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '').lower()
    with conectar_bd() as conn:
        cursor = conn.cursor()
        if termo:
            query = "SELECT * FROM profissionais WHERE (nome LIKE ? OR especialidade LIKE ?) AND validado = 1"
            resultados = cursor.execute(query, (f'%{termo}%', f'%{termo}%')).fetchall()
        else:
            resultados = cursor.execute("SELECT * FROM profissionais WHERE validado = 1").fetchall()
    return render_template('buscar.html', profissionais=resultados, busca=termo)

@app.route('/cadastro')
def exibir_cadastro():
    """Exibe o formulário de cadastro (O rosto da página)"""
    return render_template('cadastro.html')

@app.route('/enviar_cadastro', methods=['POST'])
def enviar_cadastro():
    """Processa os dados do formulário (O motor)"""
    nome = request.form.get('nome')
    localidade = request.form.get('localidade')
    especialidade = request.form.get('especialidade')
    valor = request.form.get('valor') 
    
    # Tratamento do arquivo de certificado
    file = request.files.get('doc')
    filename = None
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    try:
        with conectar_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO profissionais (nome, especialidade, valor_servico, localidade, stellar_pubkey, certificado_path)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome, especialidade, valor, localidade, 'CHAVE_STELLAR_AUTO', filename))
            conn.commit()
        
        return redirect(url_for('confirmacao_cadastro_sucesso'))
    
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        flash("Erro ao realizar cadastro. Verifique se o nome já existe.", "danger")
        return redirect(url_for('exibir_cadastro'))

@app.route('/cadastro_sucesso')
def confirmacao_cadastro_sucesso():
    """Exibe a página de sucesso após o cadastro"""
    return render_template('confirmacao_cadastro.html')

@app.route('/pagamento/<int:id>')
def pagamento(id):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        prof = cursor.execute("SELECT * FROM profissionais WHERE id = ?", (id,)).fetchone()
    
    if not prof:
        flash("Profissional não encontrado!", "danger")
        return redirect(url_for('buscar'))
        
    return render_template('pagamento.html', prof=prof)

@app.route('/confirmar_pagamento/<int:id>')
def confirmar_pagamento(id):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        prof = cursor.execute("SELECT * FROM profissionais WHERE id = ?", (id,)).fetchone()
    
    if not prof:
        return "Profissional não encontrado", 404

    valor_total = float(prof['valor_servico'])
    
    return render_template('blockchain_confirm.html', 
                           nome=prof['nome'],
                           especialidade=prof['especialidade'],
                           prof_val=valor_total * 0.80, 
                           assoc_val=valor_total * 0.15,
                           total=valor_total,
                           chave=prof['stellar_pubkey'])

if __name__ == "__main__":
    app.run(debug=True)