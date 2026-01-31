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
    # Tabela de Profissionais
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
    # Tabela de Agendamentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente TEXT,
            endereco TEXT,
            horario TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

# Inicializa o banco ao rodar o app
configurar_tabela()

# --- AUXILIARES ---
def buscar_profissional_por_id(id):
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM profissionais WHERE id = ?", (id,))
        return cursor.fetchone()

# --- ROTAS DE FLUXO ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/buscar')
def buscar():
    busca = request.args.get('q', '')
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        if busca:
            cursor.execute("""
                SELECT * FROM profissionais 
                WHERE validado = 1 AND (nome LIKE ? OR especialidade LIKE ? OR localidade LIKE ?)
            """, (f'%{busca}%', f'%{busca}%', f'%{busca}%'))
        else:
            cursor.execute("SELECT * FROM profissionais WHERE validado = 1")
        profissionais = cursor.fetchall()
    return render_template('buscar.html', profissionais=profissionais, busca=busca)

@app.route('/enviar_cadastro', methods=['POST'])
def cadastrar_profissional():
    nome = request.form.get('nome')
    especialidade = request.form.get('especialidade')
    localidade = request.form.get('localidade')
    
    valor = 0.0
    caminho_certificado = ""

    try:
        valor_str = request.form.get('valor_servico')
        if valor_str:
            valor = float(valor_str.replace(',', '.'))
    except (ValueError, TypeError):
        valor = 0.0

    arquivo = request.files.get('certificado')
    if arquivo and arquivo.filename != '':
        nome_arquivo = secure_filename(f"{nome}_{arquivo.filename}")
        caminho_certificado = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        arquivo.save(caminho_certificado)

    try:
        with conectar_bd() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id FROM profissionais WHERE nome = ?", (nome,))
            if cursor.fetchone():
                flash(f"O profissional '{nome}' já possui um cadastro pendente ou ativo.", "danger")
                return redirect(url_for('cadastro'))

            cursor.execute("""
                INSERT INTO profissionais (nome, especialidade, valor_servico, localidade, validado, certificado_path)
                VALUES (?, ?, ?, ?, 0, ?)
            """, (nome, especialidade, valor, localidade, caminho_certificado))
            conexao.commit()
            
        flash("Cadastro enviado com sucesso! Aguarde a validação.", "success")
    except Exception as e:
        flash(f"Erro inesperado: {str(e)}", "danger")

    return redirect(url_for('home'))

# --- ÁREA ADMINISTRATIVA ---

@app.route('/admin')
def admin_geral():
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        # Profissionais aguardando validação
        cursor.execute("SELECT * FROM profissionais WHERE validado = 0")
        pendentes = cursor.fetchall()
        
        # Profissionais já aprovados
        cursor.execute("SELECT * FROM profissionais WHERE validado = 1")
        validados = cursor.fetchall()
        
        # Agendamentos para o dashboard (Simulados ou do BD)
        agendamentos_ficticios = [
            {'iniciais': 'MA', 'paciente': 'Maria Andrade', 'endereco': 'Rua Flores, 123', 'horario': '09:00', 'status': 'Confirmado'},
            {'iniciais': 'JS', 'paciente': 'João Silva', 'endereco': 'Av. Central, 450', 'horario': '14:30', 'status': 'Pendente'}
        ]

    return render_template('admin.html', 
                           profissionais=pendentes, 
                           validados=validados, 
                           agendamentos=agendamentos_ficticios)

@app.route('/admin/financeiro', endpoint='admin_financas')
def admin_financas():
    dados = {
        'total_fundo': 5420.50,
        'total_pros': 12,
        'transacoes': [
            {'data': '30/01', 'tipo': 'Recebimento', 'valor': 150.00, 'cor': 'text-green-600'},
            {'data': '29/01', 'tipo': 'Repasse Prof.', 'valor': -120.00, 'cor': 'text-red-600'},
            {'data': '28/01', 'tipo': 'Taxa Social', 'valor': 15.00, 'cor': 'text-green-600'}
        ]
    }
    return render_template('admin_financas.html', **dados)

# --- AÇÕES ---

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
    # Simulação de geração de chave pública Stellar
    chave_fake = f"GB{id}STELLAR" + ("X" * (56 - len(f"GB{id}STELLAR")))
    with conectar_bd() as conexao:
        cursor = conexao.cursor()
        cursor.execute("UPDATE profissionais SET stellar_pubkey = ? WHERE id = ?", (chave_fake, id))
        conexao.commit()
    flash("Carteira Stellar ativada!", "success")
    return redirect(url_for('admin_geral'))

@app.route('/pagamento/<int:id>')
def pagamento(id):
    profissional = buscar_profissional_por_id(id)
    if not profissional:
        flash("Profissional não encontrado.", "warning")
        return redirect(url_for('home'))
    
    valor = profissional['valor_servico']
    return render_template('pagamento.html', 
                           nome=profissional['nome'],
                           total=valor,
                           prof_val=valor * 0.8,
                           assoc_val=valor * 0.15,
                           start_val=valor * 0.05,
                           chave=profissional['stellar_pubkey'])

if __name__ == "__main__":
    app.run(debug=True, port=5000)