# 🏥 Vizinhança Cuidadora: Tecnologia para o Cuidado Hiperlocal

A **Vizinhança Cuidadora** é uma plataforma de impacto social desenvolvida para conectar profissionais de saúde e cuidadores a moradores de suas próprias comunidades. O projeto foca em **segurança**, **economia circular** e **inclusão digital**, transformando a Associação de Moradores no selo de confiança do ecossistema.

---

## 🚀 Diferenciais Técnicos e Pontos Fortes

### 1. Validação Social (Governança de Dados)
Diferente de plataformas de serviços comuns, o projeto implementa um fluxo de aprovação obrigatório:

* **Armazenamento de Credenciais**: O sistema permite o upload de certificados profissionais via `multipart/form-data`, salvando-os em um diretório seguro para auditoria.
* **Status de Visibilidade**: Implementamos uma lógica de banco de dados onde o profissional só é indexado na busca após a alteração do campo **validado** de **0** para **1** pela Associação de Moradores no painel administrativo (`/admin`).

### 2. Algoritmo de Hiperlocalidade
O motor de busca foi otimizado para a realidade das comunidades:

* **Filtro por Setores**: A consulta SQL utiliza o operador `LIKE` para permitir buscas flexíveis por **nome**, **especialidade** ou **setor específico**, garantindo que o cuidado esteja a poucos metros de distância do morador.
* **Baixa Latência**: Utilização do **SQLite** para garantir respostas rápidas mesmo em conexões de internet limitadas.

### 3. Modelo de Economia Circular (Fintech Social)
O código fonte traduz o plano de negócios diretamente na interface do usuário através de um simulador de repasse automático:

* **Repasse Direto (80%)**: Focado na autonomia financeira do profissional local.
* **Taxa de Sustentabilidade (15%)**: Destinada à manutenção tecnológica da startup.
* **Fundo Comunitário (5%)**: Reinvestimento direto na Associação de Moradores para melhorias na infraestrutura física do bairro.

### 4. Arquitetura "Mobile-First" e Acessível
O frontend foi desenvolvido com foco em inclusão:

* **UX Intuitiva**: Botões grandes, cores contrastantes (**Verde Confiança**) e navegação simplificada para usuários com diferentes níveis de literacia digital.
* **Tecnologias Utilizadas**: **Python**, **Flask** (Backend), **SQLite** (Banco de Dados), **HTML5** e **CSS3** (Frontend).

---

## 🛠️ Como Executar o MVP

1.  **Clone o repositório**:
    ```bash
    git clone [https://github.com/SEU_USUARIO/vizinhanca-cuidadora.git](https://github.com/SEU_USUARIO/vizinhanca-cuidadora.git)
    ```

2.  **Instale as dependências**:
    ```bash
    pip install flask
    ```

3.  **Inicie o servidor**:
    ```bash
    python app.py
    ```

4.  **Acesse as rotas**:
    * **Cadastro**: `localhost:5000/`
    * **Painel de Validação**: `localhost:5000/admin`
    * **Busca de Profissionais**: `localhost:5000/buscar`

---

## 📈 Roadmap: Próximos Passos (Evolução do Produto)

O projeto **Vizinhança Cuidadora** foi desenhado para crescer. Abaixo estão as funcionalidades planejadas para as próximas versões:

### Fase 1: Segurança e Pagamento (Curto Prazo)
* **Integração com PIX API**: Automação total da divisão de valores (**80/15/5**) no momento do pagamento, eliminando processos manuais.
* **Sistema de Avaliações (Rating)**: Implementação de sistema de "estrelas" e comentários para que moradores avaliem o atendimento, aumentando a confiança na rede.
* **Chat Interno**: Canal de comunicação direto e seguro entre morador e profissional dentro da plataforma para agendamento de visitas.

### Fase 2: Engajamento e Expansão (Médio Prazo)
* **Dashboard para a Associação**: Gráficos de impacto social mostrando quanto de renda foi gerada para o bairro e quanto o fundo comunitário arrecadou.
* **Notificações via WhatsApp**: Integração para avisar profissionais sobre novas solicitações de atendimento e associações sobre novos cadastros pendentes.
* **Perfil Multidisciplinar**: Expansão para outras áreas além da saúde, como pequenos reparos domésticos e apoio pedagógico.

### Fase 3: Inteligência e Dados (Longo Prazo)
* **Mapa de Calor de Demandas**: Uso de ciência de dados para identificar quais especialidades de saúde estão em falta em cada setor da comunidade, orientando cursos de capacitação.
* **App Nativo (Android/iOS)**: Desenvolvimento de aplicativo móvel para facilitar o acesso offline e uso de geolocalização em tempo real.