# 🏠 Vizinhança Cuidadora

![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey)
![Blockchain](https://img.shields.io/badge/Blockchain-Stellar-purple)

Uma plataforma comunitária que conecta profissionais de saúde e apoio a moradores locais, utilizando a **Blockchain Stellar** para garantir pagamentos transparentes e a sustentabilidade de um fundo social comunitário.

---

## 🚀 Sobre o Projeto

O **Vizinhança Cuidadora** descentraliza a contratação de serviços de cuidado. O sistema permite uma curadoria rigorosa de profissionais e uma distribuição de valores automatizada, onde cada transação beneficia não apenas o cuidador, mas toda a comunidade local.

### 💸 O Modelo de Impacto (Split de Pagamento)
Para cada serviço contratado, o valor é dividido automaticamente:
* **80%**: Destinado diretamente ao **Profissional**.
* **15%**: Reinvestido no **Fundo Comunitário** da vizinhança.
* **5%**: Taxa de **operação e manutenção** da rede.



---

## 🛠️ Tecnologias Utilizadas

* **Backend**: Python 3.9+ com Flask.
* **Banco de Dados**: SQLite3 para persistência local.
* **Frontend**: HTML5, Jinja2 e Tailwind CSS.
* **Blockchain**: Integração com a rede Stellar (Simulação via Public Keys).
* **Gráficos**: Chart.js para monitoramento financeiro.

---

## 📦 Funcionalidades Implementadas

### 👤 Usuário (Morador)
- [x] **Busca Inteligente**: Filtros por nome, especialidade ou bairro.
- [x] **Checkout Transparente**: Resumo detalhado da distribuição do pagamento.
- [x] **Segurança**: Acesso apenas a profissionais com certificados validados.

### 🏥 Profissional (Cuidador)
- [x] **Onboarding Digital**: Upload seguro de certificados profissionais.
- [x] **Carteira Digital**: Vinculação de Chave Pública Stellar para recebimentos.

### 🛡️ Administrativo
- [x] **Gestão de Aprovações**: Interface para validar documentos e habilitar profissionais.
- [x] **Dashboard Financeiro**: Gráficos de crescimento do fundo e histórico de transações.

---

## 📋 Como Instalar e Rodar

1.  **Clone o repositório**:
    ```bash
    git clone [https://github.com/seu-usuario/vizinhanca-cuidadora.git](https://github.com/seu-usuario/vizinhanca-cuidadora.git)
    cd vizinhanca-cuidadora
    ```

2.  **Configure o ambiente virtual**:
    ```bash
    python -m venv venv
    # Ative o venv:
    # Windows: venv\Scripts\activate | Linux/Mac: source venv/bin/activate
    ```

3.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação**:
    ```bash
    python app.py
    ```
    Acesse em: `http://127.0.0.1:5000`.

---

## 🏗️ Estrutura do Projeto

```text
├── app.py              # Servidor Flask e rotas principais
├── vizinhanca.db       # Banco de dados SQLite
├── /templates          # Páginas HTML (Admin, Buscar, Pagamento)
├── /static             # Ativos estáticos (Imagens, CSS, JS)
├── /certificados       # Documentos enviados (protegido por .gitignore)
└── .gitignore          # Regras de exclusão de arquivos sensíveis
Este projeto está sob a licença MIT.