# 🏥 Vizinhança Cuidadora: Tecnologia para o Cuidado Hiperlocal

A **Vizinhança Cuidadora** é uma plataforma de impacto social (**Socialtech**) que conecta profissionais de saúde e cuidadores a moradores de suas próprias comunidades. O projeto utiliza tecnologia **Blockchain (Web3)** para garantir transparência e um modelo de **Economia Circular** para fortalecer associações de moradores.

---

## 🌟 Diferenciais Técnicos e Pontos Fortes

### 🛡️ 1. Governança e Validação Social
O sistema implementa um fluxo de aprovação obrigatório via painel administrativo (`/admin`). O profissional só é indexado na busca após a **Associação de Moradores validar suas credenciais**, transformando a associação no "selo de confiança" da rede.

### 💰 2. Fintech Social & Divisão Automática (80/15/5)
O algoritmo de pagamento traduz o plano de negócios diretamente na interface, realizando o repasse automático:
* **80% (Repasse Direto):** Autonomia financeira para o profissional local.
* **15% (Fundo Comunitário):** Reinvestimento direto na Associação de Moradores.
* **5% (Plataforma):** Manutenção da infraestrutura tecnológica.

### ⛓️ 3. Integração com Blockchain Stellar
Diferente de sistemas comuns, utilizamos a rede **Stellar** para criar uma camada de confiança descentralizada:
* **Identidade Digital:** Geração automática de chaves públicas e privadas para cada profissional.
* **Financiamento Testnet:** Integração com o *Friendbot* para ativação automática de contas com ativos de teste.
* **Segurança de Chaves:** Exibição encurtada de endereços (Ex: `GD72...W3P2`) para melhor UX.

### 📱 4. Arquitetura Mobile-First e Acessível
Interface desenvolvida com foco em inclusão digital:
* **UX Intuitiva:** Botões grandes e cores contrastantes para diversos níveis de literacia digital.
* **Segurança:** Uso de `.gitignore` para proteger dados sensíveis e o banco de dados `vizinhanca.db`.

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
| :--- | :--- |
| **Backend** | Python 3.x / Flask |
| **Banco de Dados** | SQLite3 |
| **Blockchain** | Stellar SDK (Testnet) |
| **Frontend** | HTML5 / CSS3 (Responsivo) |

---

## 💻 Como Executar o MVP

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/vizinhanca-cuidadora.git](https://github.com/SEU_USUARIO/vizinhanca-cuidadora.git)
   cd vizinhanca-cuidadora