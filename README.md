# NextMind

**Infraestrutura de Inteligência Cognitiva** - Uma plataforma unificada e local-first para gerenciar conversas com múltiplas IAs.

## 🎯 Visão Geral

NextMind é uma plataforma desktop que permite organizar e gerenciar conversas com múltiplos provedores de IA (GPT, Claude, Gemini, modelos locais) em um único lugar, com foco em privacidade e organização baseada em projetos.

### Princípios
- **Local-First & Privacy-First**: Todos os dados residem localmente (SQLite)
- **Agnóstico ao Provedor**: Suporte para OpenAI, Anthropic, Google, OpenRouter e modelos locais
- **Power User UX**: Interface eficiente com atalhos de teclado e organização densa
- **Estruturado e Flexível**: Suporta projetos organizados e conversas rápidas

## 📁 Estrutura do Projeto

Este projeto segue a arquitetura de 3 camadas definida em `AGENTS_V1.0.md`:

```
nextmind/
├── directives/          # Camada 1: Diretivas (SOPs em Markdown)
│   └── database_management.md
├── execution/           # Camada 2: Scripts Python determinísticos
│   ├── database.py
│   ├── schema.sql
│   ├── import_chatgpt.py
│   ├── import_claude.py
│   └── test_database.py
├── ui/                  # Interface Electron + React + TypeScript
│   ├── electron/        # Processo principal do Electron
│   ├── src/             # Frontend React
│   └── package.json
├── .tmp/                # Arquivos temporários e logs
│   ├── data/            # Banco de dados SQLite
│   └── logs/            # Logs de execução e decisões
├── chats/               # Arquivos JSON de importação
├── .env.example         # Template de variáveis de ambiente
└── PRD.md               # Documento de Requisitos do Produto
```

## 🚀 Setup

### Pré-requisitos
- Python 3.8+
- Node.js 18+
- npm ou yarn

### 1. Backend (Python)

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências (se houver requirements.txt)
pip install -r requirements.txt

# Inicializar banco de dados
python -c "from execution.database import Database; db = Database(); db.initialize_schema()"
```

### 2. Frontend (Electron + React)

```bash
cd ui
npm install
npm run dev  # Modo desenvolvimento
```

## 📊 Banco de Dados

O NextMind utiliza SQLite para armazenamento local:
- **Schema**: `execution/schema.sql`
- **Modelos**: `execution/database.py`
- **Localização**: `.tmp/data/nextmind.db`

### Importação de Dados

```bash
# Importar conversas do ChatGPT
python execution/import_chatgpt.py

# Importar conversas do Claude
python execution/import_claude.py
```

Os arquivos JSON devem estar em `chats/conversations gpt.json` e `chats/conversations claude.json`.

## 🏗️ Arquitetura de 3 Camadas

### Camada 1: Directives (O que fazer)
SOPs em Markdown que definem objetivos, inputs, outputs e edge cases.

### Camada 2: Orchestration (Tomada de decisão)
Agentes IA fazem roteamento inteligente, leem directives e chamam scripts.

### Camada 3: Execution (Execução)
Scripts Python determinísticos que fazem o trabalho pesado (API calls, DB operations).

**Vantagem**: Separação entre lógica probabilística (IA) e determinística (código), aumentando confiabilidade.

## 📝 Documentação

- **PRD.md**: Documento de Requisitos do Produto
- **AGENTS_V1.0.md**: Guia de arquitetura e instruções para agentes
- **directives/**: Procedimentos operacionais padrão

## 🔐 Segurança

- Chaves de API armazenadas localmente (BYOK - Bring Your Own Key)
- Dados nunca saem do dispositivo
- `.env` nunca commitado (use `.env.example` como template)

## 📋 Roadmap

### Fase 1: MVP (Core & CLI) ✅
- [x] Estrutura do Projeto e Banco de Dados
- [x] Scripts de Ingestão (ChatGPT/Claude)
- [x] Interface Electron básica

### Fase 2: UI & Contexto (Em Progresso)
- [ ] Interface Gráfica completa
- [ ] Barra Lateral (Projetos vs Chats)
- [ ] Gestão de Arquivos de Contexto por Projeto

### Fase 3: Advanced
- [ ] Agentes Autônomos
- [ ] RAG Local (Vector Database)

## 📄 Licença

[Definir licença]
