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
        return render_template('index.html', profissionais=resultados, busca_feita=True)
    
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

# --- ROTAS ADMINISTRATIVAS ---
@app.route('/admin/financeiro')
def admin_financeiro():
    """Painel de controle do Fundo Comunitário (15%)"""
    with conectar_bd() as conn:
        cursor = conn.cursor()
        
        # 1. Contagem de profissionais ativos
        total_pros = cursor.execute("SELECT COUNT(*) FROM profissionais WHERE validado = 1").fetchone()[0]
        
        # 2. Simulação de Saldo do Fundo (No mundo real, viria da API da Stellar)
        # Aqui somamos 15% de todos os valores de serviços de profissionais validados
        total_fundo = cursor.execute("SELECT SUM(valor_servico * 0.15) FROM profissionais WHERE validado = 1").fetchone()[0] or 0.0
        
        # 3. Histórico de Transações Fake (Simulando dados da Blockchain)
        transacoes = [
            {'data': '07/02/2026 09:45', 'tipo': 'Contribuição Social', 'valor': 15.00, 'cor': 'text-green-600'},
            {'data': '06/02/2026 14:20', 'tipo': 'Contribuição Social', 'valor': 22.50, 'cor': 'text-green-600'},
            {'data': '05/02/2026 18:10', 'tipo': 'Compra Kit Primeiros Socorros', 'valor': -150.00, 'cor': 'text-red-600'}
        ]

    return render_template('admin_financas.html', 
                           total_pros=total_pros, 
                           total_fundo=total_fundo, 
                           transacoes=transacoes)

# Atalho para o Painel Geral (que você já tinha)
@app.route('/admin/geral')
def admin_geral():
    return redirect(url_for('admin'))

@app.route('/admin')
def admin():
    """Lista todos os profissionais para curadoria"""
    with conectar_bd() as conn:
        cursor = conn.cursor()
        # Buscamos todos para o admin poder gerenciar
        profissionais = cursor.execute("SELECT * FROM profissionais ORDER BY validado ASC").fetchall()
    return render_template('admin.html', profissionais=profissionais)

@app.route('/validar_profissional/<int:id>')
def validar_profissional(id):
    """Aprova o profissional para aparecer nas buscas"""
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE profissionais SET validado = 1 WHERE id = ?", (id,))
        conn.commit()
    flash("Profissional aprovado com sucesso!", "success")
    return redirect(url_for('admin'))

@app.route('/excluir_profissional/<int:id>')
def excluir_profissional(id):
    """Remove o profissional do banco de dados"""
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM profissionais WHERE id = ?", (id,))
        conn.commit()
    flash("Profissional removido da base.", "info")
    return redirect(url_for('admin'))

@app.route('/criar_carteira/<int:id>')
def criar_carteira(id):
    """Simula a criação de uma chave Stellar (Blockchain)"""
    import uuid
    nova_chave = f"GD{uuid.uuid4().hex[:48].upper()}" # Simulação de chave pública
    
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE profissionais SET stellar_pubkey = ? WHERE id = ?", (nova_chave, id))
        conn.commit()
    
    flash(f"Carteira Stellar ativada: {nova_chave[:10]}...", "success")
    return redirect(url_for('admin'))

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