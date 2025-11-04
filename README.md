# 🤖 Julius Financeiro

Um bot do Telegram inteligente que ajuda você a registrar suas despesas diárias de forma natural usando Inteligência Artificial (Claude da Anthropic) e integração automática com Google Sheets.

## 🌟 Funcionalidades

- ✅ Conversa natural em português brasileiro
- 💰 Detecção automática de despesas nas mensagens
- 📊 Registro automático no Google Sheets
- 🏷️ Categorização inteligente de despesas
- 📈 Estatísticas mensais detalhadas
- 📅 Suporte a datas relativas ("ontem", "domingo passado")
- 🔍 Consulta de gastos por comando ou linguagem natural

## 🎯 Como Funciona

1. Você envia uma mensagem para o bot contando sobre um gasto
2. O Claude (IA da Anthropic) analisa sua mensagem e extrai:
   - Valor da despesa
   - Data (se mencionada, senão usa hoje)
   - Categoria (alimentação, transporte, saúde, etc.)
   - Descrição adicional
3. O bot registra automaticamente na sua planilha do Google Sheets

### Exemplos de uso:
```
Você: Gastei 45 reais no almoço hoje
Bot: ✅ Despesa registrada! R$ 45,00 em Alimentação

Você: Domingo passado gastei 120 de Uber
Bot: ✅ Despesa registrada! R$ 120,00 em Transporte (30/10/2025)

Você: quanto gastei esse mês?
Bot: 📊 Estatísticas de Novembro/2025
     💰 Total gasto: R$ 1.234,56
     ...
```

## 📁 Estrutura do Projeto
```
julius-financeiro/
├── julius.py                              # Entrada principal do bot
├── config.py                              # Configurações e variáveis de ambiente
├── pyproject.toml                         # Dependências do Poetry
├── handlers/
│   ├── commands.py                        # Handlers de comandos (/start, /help, /stats)
│   └── messages.py                        # Handler de mensagens de texto
├── services/
│   ├── claude_service.py                  # Integração com Claude AI
│   └── sheets_service.py                  # Integração com Google Sheets
├── utils/
│   └── constants.py                       # Constantes (emojis, categorias, etc)
├── julius-financeiro-credentials.json     # Credenciais do Google (não commitar!)
└── .env                                   # Variáveis de ambiente (não commitar!)
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- [Poetry](https://python-poetry.org/docs/#installation) instalado
- Conta no Telegram
- Conta na Anthropic (para usar a API do Claude)
- Conta Google (para Google Sheets)

### Passo 1: Clonar e Instalar Dependências
```bash
# Clone o repositório (ou baixe os arquivos)
git clone <seu-repositorio>
cd julius-financeiro

# Instale as dependências com Poetry
poetry install
```

### Passo 2: Criar o Bot no Telegram

1. Abra o Telegram e procure por `@BotFather`
2. Envie o comando `/newbot`
3. Escolha um nome para seu bot (ex: "Julius Financeiro")
4. Escolha um username (deve terminar com 'bot', ex: "julius_financeiro_bot")
5. Copie o token que o BotFather forneceu

### Passo 3: Obter a API Key da Anthropic

1. Acesse https://console.anthropic.com/
2. Crie uma conta ou faça login
3. Vá em "API Keys"
4. Clique em "Create Key"
5. Copie a chave gerada

### Passo 4: Configurar Google Sheets

#### 4.1 Criar a Planilha

1. Acesse https://docs.google.com/spreadsheets/
2. Crie uma nova planilha
3. Na primeira linha (cabeçalho), adicione as colunas:
   - **A1:** `Data`
   - **B1:** `Valor`
   - **C1:** `Categoria`
   - **D1:** `Descrição`
4. Copie o ID da planilha da URL (a parte entre `/d/` e `/edit`)
   - Exemplo: `https://docs.google.com/spreadsheets/d/`**`1A2B3C4D5E6F`**`/edit`

#### 4.2 Criar Service Account no Google Cloud

1. Acesse https://console.cloud.google.com/
2. Crie um novo projeto ou selecione um existente
3. Vá em "APIs & Services" > "Library"
4. Procure e ative a **"Google Sheets API"**
5. Vá em "APIs & Services" > "Credentials"
6. Clique em "Create Credentials" > "Service Account"
7. Preencha o nome do service account e clique em "Create"
8. Clique em "Continue" (não precisa adicionar roles)
9. Clique em "Done"
10. Na lista de service accounts, clique no **email** do service account criado
11. Vá na aba "Keys"
12. Clique em "Add Key" > "Create new key"
13. Escolha **"JSON"** e clique em "Create"
14. O arquivo JSON será baixado automaticamente

#### 4.3 Compartilhar a Planilha

1. Abra o arquivo JSON baixado
2. Copie o email do service account (campo `"client_email"`)
3. Volte para sua planilha do Google Sheets
4. Clique em "Compartilhar"
5. Cole o email do service account
6. Dê permissão de **"Editor"**
7. Desmarque "Notificar pessoas"
8. Clique em "Compartilhar"

### Passo 5: Configurar Variáveis de Ambiente

1. Crie um arquivo `.env` na raiz do projeto:
```bash
touch .env
```

2. Adicione suas credenciais ao `.env`:
```env
TELEGRAM_BOT_TOKEN=seu_token_do_telegram_aqui
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
GOOGLE_SHEET_ID=id_da_sua_planilha_aqui
GOOGLE_CREDENTIALS_FILE=julius-financeiro-credentials.json
```

3. Renomeie o arquivo JSON baixado do Google para `julius-financeiro-credentials.json` e coloque na raiz do projeto

### Passo 6: Executar o Bot
```bash
# Executar com Poetry
poetry run python julius.py

# Ou ative o ambiente virtual primeiro
poetry shell
python julius.py
```

Você deve ver:
```
==================================================
🤖 Julius Financeiro
==================================================
✅ Bot iniciado com sucesso!
📊 Integração com Google Sheets ativa
🤖 Claude AI integrado
==================================================
```

## 📱 Usando o Bot

### Comandos Disponíveis

- `/start` - Inicia o bot e mostra as boas-vindas
- `/help` - Mostra ajuda e exemplos de uso
- `/stats` - Mostra estatísticas do mês atual

### Registrando Despesas

Basta conversar naturalmente com o bot! Exemplos:

**Despesas simples:**
- "Gastei 45 reais no almoço"
- "R$ 120 no Uber"
- "Comprei remédio por 78,50"

**Com datas relativas:**
- "Ontem gastei 50 reais no cinema"
- "Domingo passado paguei 200 de supermercado"
- "Segunda-feira gastei 35 de almoço"

**Consultar gastos:**
- "quanto gastei esse mês?"
- "me mostra as estatísticas"
- "status do mês"

### Categorias Reconhecidas

O bot categoriza automaticamente suas despesas em:

- 🍽️ **Alimentação** - Restaurantes, supermercado, delivery
- 🚕 **Transporte** - Uber, gasolina, estacionamento
- 💊 **Saúde** - Remédios, consultas, exames
- 🎬 **Lazer** - Cinema, jogos, entretenimento
- 🏡 **Moradia** - Aluguel, contas, manutenção
- 📖 **Educação** - Cursos, livros, material escolar
- 🛒 **Compras** - Roupas, eletrônicos, diversos
- 📦 **Outros** - Outras despesas

## 📊 Estrutura da Planilha

O bot adiciona automaticamente linhas com os valores armazenados como números (não formatados):

| Data | Valor | Categoria | Descrição |
|------|-------|-----------|-----------|
| 04/11/2025 | 45.50 | Alimentação | Almoço |
| 04/11/2025 | 120.00 | Transporte | Uber |

> **Nota:** Os valores são armazenados como números para facilitar cálculos. Você pode formatar as células como moeda no Google Sheets.

## 🔒 Segurança

⚠️ **IMPORTANTE:**
- Nunca commite o arquivo `.env`
- Nunca commite o arquivo `julius-financeiro-credentials.json`
- Adicione ambos ao `.gitignore`
```gitignore
# .gitignore
.env
*.json
__pycache__/
*.pyc
.venv/
```

## 🛠️ Desenvolvimento

### Adicionar Dependências
```bash
# Adicionar nova dependência
poetry add nome-do-pacote

# Adicionar dependência de desenvolvimento
poetry add --group dev nome-do-pacote
```

### Estrutura de Código

- **`config.py`** - Gerencia variáveis de ambiente e validação
- **`handlers/`** - Contém todos os handlers do Telegram
- **`services/`** - Serviços externos (Claude, Google Sheets)
- **`utils/`** - Constantes e funções auxiliares

### Personalizações

**Adicionar novas categorias:**
Edite o arquivo `utils/constants.py` e adicione na lista `CATEGORIES` e no dicionário `CATEGORY_EMOJIS`.

**Modificar o comportamento do Claude:**
Ajuste o `system_prompt` em `services/claude_service.py`.

## ❓ Troubleshooting

### Erro: "TELEGRAM_BOT_TOKEN não encontrado"
- Verifique se o arquivo `.env` existe na raiz do projeto
- Confirme se as variáveis estão sem espaços: `CHAVE=valor`

### Erro de autenticação do Google Sheets
- Verifique se o service account tem permissão de **Editor** na planilha
- Confirme se o arquivo `julius-financeiro-credentials.json` está correto
- Verifique se a **Google Sheets API** está ativada no projeto

### Bot não responde
- Confirme se o token do Telegram está correto
- Verifique se o bot está rodando (`poetry run python julius.py`)
- Teste com o comando `/start`

### Claude não identifica despesas
- Verifique se a API Key da Anthropic está correta
- Confirme se você tem créditos na conta Anthropic
- Tente reformular a mensagem de forma mais clara

### Erros com Poetry
```bash
# Limpar cache e reinstalar
poetry cache clear pypi --all
poetry install
```

## 📝 Licença

Este projeto é de uso pessoal. Sinta-se livre para modificar conforme suas necessidades!

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Abra uma issue ou pull request.

---

**Desenvolvido com ❤️ para ajudar no controle financeiro pessoal**

**Tecnologias:** Python • Poetry • Telegram Bot API • Claude AI (Anthropic) • Google Sheets API