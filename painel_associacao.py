from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Configuração de pastas
UPLOAD_FOLDER = 'certificados'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- BANCO DE DADOS ---
def conectar_bd():
    return sqlite3.connect('vizinhanca.db')

def inicializar_bd():
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profissionais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                especialidade TEXT NOT NULL,
                localidade TEXT NOT NULL,
                validado INTEGER DEFAULT 0 
            )
        ''')
        conexao.commit()

# --- ROTAS DE NAVEGAÇÃO ---

@app.route('/')
@app.route('/cadastro') # Agora o Flask reconhece as duas URLs
def pagina_inicial():
    return render_template('cadastro.html')

@app.route('/enviar_cadastro', methods=['POST'])
def processar_cadastro():
    nome = request.form.get('nome')
    especialidade = request.form.get('especialidade')
    localidade = request.form.get('localidade')
    
    # Upload do arquivo
    arquivo = request.files.get('certificado')
    if arquivo and arquivo.filename != '':
        arquivo.save(os.path.join(UPLOAD_FOLDER, arquivo.filename))

    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO profissionais (nome, especialidade, localidade, validado)
            VALUES (?, ?, ?, 0)
        ''', (nome, especialidade, localidade))
        conexao.commit()
    
    return "<h1>✅ Cadastro enviado com sucesso!</h1><br><a href='/'>Voltar</a>"

# --- PAINEL ADMINISTRATIVO (ASSOCIAÇÃO) ---

@app.route('/admin')
def painel_admin():
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, especialidade, localidade FROM profissionais WHERE validado = 0")
        pendentes = cursor.fetchall()
    return render_template('admin.html', profissionais=pendentes)

@app.route('/validar/<int:id>')
def validar_profissional(id):
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute("UPDATE profissionais SET validado = 1 WHERE id = ?", (id,))
        conexao.commit()
    return redirect(url_for('painel_admin'))

@app.route('/excluir/<int:id>')
def excluir_profissional(id):
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM profissionais WHERE id = ?", (id,))
        conexao.commit()
    return redirect(url_for('painel_admin'))

# --- BUSCA E ECONOMIA CIRCULAR ---

@app.route('/buscar')
def buscar_profissionais():
    termo = request.args.get('q', '')
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        if termo:
            cursor.execute("""
                SELECT nome, especialidade, localidade 
                FROM profissionais 
                WHERE validado = 1 AND (nome LIKE ? OR localidade LIKE ? OR especialidade LIKE ?)
            """, ('%' + termo + '%', '%' + termo + '%', '%' + termo + '%'))
        else:
            cursor.execute("SELECT nome, especialidade, localidade FROM profissionais WHERE validado = 1")
        resultados = cursor.fetchall()
    return render_template('buscar.html', profissionais=resultados, busca=termo)

@app.route('/pagamento/<nome_prof>')
def resumo_pagamento(nome_prof):
    """Demonstrativo do Modelo de Negócio 80/15/5"""
    valor_total = 100.00
    profissional = valor_total * 0.80
    startup = valor_total * 0.15
    associacao = valor_total * 0.05
    
    return f"""
    <div style="font-family: 'Segoe UI', sans-serif; max-width: 400px; margin: 50px auto; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 6px solid #27ae60;">
        <h2 style="color: #2c3e50;">Resumo do Cuidado</h2>
        <p>Profissional: <strong>{nome_prof}</strong></p>
        <hr style="border: 0; border-top: 1px solid #eee;">
        <p><strong>Valor Total:</strong> R$ {valor_total:.2f}</p>
        <div style="background: #f9f9f9; padding: 10px; border-radius: 8px;">
            <p style="color: #27ae60; margin: 5px 0;">💰 <strong>R$ {profissional:.2f}</strong> para o Vizinho</p>
            <p style="color: #2980b9; margin: 5px 0;">🚀 <strong>R$ {startup:.2f}</strong> para a Startup</p>
            <p style="color: #f39c12; margin: 5px 0;">🏠 <strong>R$ {associacao:.2f}</strong> para a Associação</p>
        </div>
        <p style="font-size: 12px; color: #7f8c8d; margin-top: 15px;">Ao confirmar, você fortalece a economia da sua comunidade.</p>
        <button onclick="alert('Pagamento processado! O profissional foi notificado.')" style="width: 100%; padding: 15px; background: #27ae60; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px;">
            Confirmar e Pagar
        </button>
        <br><br>
        <a href='/buscar' style="color: #95a5a6; text-decoration: none; display: block; text-align: center;">← Voltar para busca</a>
    </div>
    """

if __name__ == '__main__':
    inicializar_bd()
    app.run(debug=True)