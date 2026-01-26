from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import requests
from stellar_sdk import Keypair

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
                valor_servico REAL DEFAULT 0.0,
                validado INTEGER DEFAULT 0,
                stellar_pubkey TEXT
            )
        ''')
        conexao.commit()

# --- ROTAS DE NAVEGAÇÃO E CADASTRO ---

@app.route('/')
@app.route('/cadastro')
def pagina_inicial():
    return render_template('cadastro.html')

@app.route('/enviar_cadastro', methods=['POST'])
def processar_cadastro():
    nome = request.form.get('nome')
    especialidade = request.form.get('especialidade')
    localidade = request.form.get('localidade')
    valor_servico = request.form.get('valor_servico', type=float)
    
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO profissionais (nome, especialidade, localidade, valor_servico, validado)
            VALUES (?, ?, ?, ?, 0)
        ''', (nome, especialidade, localidade, valor_servico))
        conexao.commit()
    return "<h1>✅ Cadastro e Preço definidos!</h1><a href='/'>Voltar</a>"

@app.route('/admin')
def painel_admin():
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        # Seleciona inclusive a chave stellar (índice 4) para o admin.html
        cursor.execute("SELECT id, nome, especialidade, localidade, stellar_pubkey FROM profissionais WHERE validado = 0")
        pendentes = cursor.fetchall()
    return render_template('admin.html', profissionais=pendentes)

# --- INTEGRAÇÃO STELLAR ---

@app.route('/criar_carteira/<int:id>')
def criar_carteira_stellar(id):
    kp = Keypair.random()
    public_key = kp.public_key
    secret = kp.secret 

    try:
        requests.get(f"https://friendbot.stellar.org/?addr={public_key}")
    except Exception as e:
        print(f"Erro ao financiar conta: {e}")

    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute("UPDATE profissionais SET stellar_pubkey = ? WHERE id = ?", (public_key, id))
        conexao.commit()
    
    return f"""
        <div style="font-family: sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; border: 2px solid #7d3cff; border-radius: 10px;">
            <h2 style="color: #7d3cff;">🌟 Carteira Stellar Criada!</h2>
            <p><strong>Dono (ID):</strong> {id}</p>
            <p><strong>Chave Pública:</strong> <br><code>{public_key}</code></p>
            <p style="color: red;"><strong>Chave Privada (SECRETA):</strong> <br><code>{secret}</code></p>
            <hr>
            <a href='/admin'>Voltar ao Painel Admin</a>
        </div>
    """

# --- BUSCA E PAGAMENTO ---

@app.route('/buscar')
def buscar_profissionais():
    termo = request.args.get('q', '')
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        query = "SELECT nome, especialidade, localidade, stellar_pubkey, valor_servico FROM profissionais WHERE validado = 1"
        if termo:
            query += " AND (nome LIKE ? OR localidade LIKE ?)"
            cursor.execute(query, ('%' + termo + '%', '%' + termo + '%'))
        else:
            cursor.execute(query)
        resultados = cursor.fetchall()
    return render_template('buscar.html', profissionais=resultados, busca=termo)

@app.route('/validar/<int:id>')
def validar_profissional(id):
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute("UPDATE profissionais SET validado = 1 WHERE id = ?", (id,))
        conexao.commit()
    return redirect(url_for('painel_admin'))

@app.route('/pagamento/<path:nome_prof>')
def resumo_pagamento(nome_prof):
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT valor_servico, stellar_pubkey FROM profissionais WHERE nome = ?", (nome_prof,))
        resultado = cursor.fetchone()
    
    if not resultado:
        return "<h1>Erro: Profissional não encontrado.</h1>"

    valor_total = resultado[0] if resultado[0] else 0.0
    chave_stellar = resultado[1] if resultado[1] else "Carteira não gerada"

    # Cálculos 80/15/5
    profissional = valor_total * 0.80
    startup = valor_total * 0.05
    associacao = valor_total * 0.15
    
    # HTML do Resumo de Pagamento com o bloco de endereço Stellar integrado
    return f"""
    <div style="font-family: 'Segoe UI', sans-serif; max-width: 450px; margin: 40px auto; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 8px solid #7d3cff; background: white;">
        <h2 style="color: #2c3e50; text-align: center;">Finalizar Pagamento</h2>
        
        <div style="background: #2c3e50; color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
            <span style="font-size: 10px; opacity: 0.8; letter-spacing: 1px;">ENDEREÇO DE DESTINO (BLOCKCHAIN)</span><br>
            <code style="font-size: 13px; color: #f1c40f; word-break: break-all;">{chave_stellar[:12]}...{chave_stellar[-12:]}</code>
        </div>

        <p>Destinatário: <strong>{nome_prof}</strong></p>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        
        <div style="display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; margin-bottom: 20px;">
            <span>Total a Pagar:</span>
            <span style="color: #27ae60;">R$ {valor_total:.2f}</span>
        </div>

        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; font-size: 14px;">
            <p style="margin: 5px 0; color: #27ae60;">💰 <strong>R$ {profissional:.2f}</strong> para o Profissional</p>
            <p style="margin: 5px 0; color: #2980b9;">🏢 <strong>R$ {associacao:.2f}</strong> para a Associação</p>
            <p style="margin: 5px 0; color: #7f8c8d;">🚀 <strong>R$ {startup:.2f}</strong> Taxa da Plataforma</p>
        </div>

        <button onclick="alert('Transação enviada para a rede Stellar!\\nValor: R$ {valor_total:.2f}\\nDestino: {chave_stellar[:10]}...')" 
                style="width: 100%; padding: 16px; background: #27ae60; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 25px;">
            Confirmar Pagamento via Stellar
        </button>
        <a href='/buscar' style="display: block; text-align: center; margin-top: 15px; color: #95a5a6; text-decoration: none; font-size: 14px;">Cancelar e Voltar</a>
    </div>
    """

if __name__ == '__main__':
    inicializar_bd()
    app.run(debug=True)