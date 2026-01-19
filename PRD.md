# Documento de Requisitos do Produto (PRD) - NextMind

## 1. Visão Geral do Produto
**Nome**: NextMind
**Slogan**: Infraestrutura de Inteligência Cognitiva (Cognitive Intelligence Infrastructure)
**Descrição**: Uma plataforma unificada e "local-first" para gerenciar conversas com múltiplas IAs (GPT, Claude, Gemini, Local Models). O NextMind permite que usuários organizem suas interações em **Projetos** com contextos específicos, atuando como um "sistema operacional" para sua memória cognitiva digital.
**Problema**: Fragmentação do histórico de conversas entre múltiplos provedores, falta de organização estruturada (projetos), e preocupações com privacidade/propriedade de dados.

## 2. Princípios de Design
1.  **Local-First & Privacy-First**: Todos os dados (conversas, chaves de API, contextos) residem localmente no dispositivo do usuário (SQLite).
2.  **Agnóstico ao Provedor**: Suporte transparente para OpenAI, Anthropic, Google, OpenRouter e Modelos Locais (Ollama).
3.  **Power User UX**: Atalhos de teclado, Markdown rico, organização densa e eficiente (inspirado em IDEs).
4.  **Estruturado e Flexível**: Suporta tanto fluxos de trabalho rígidos baseados em Projetos quanto conversas rápidas e descartáveis.

## 3. Requisitos Funcionais

### 3.1. Gestão de Identidade e Conectividade (BYOK)
- **Gerenciamento de Chaves (BYOK)**: O usuário insere suas próprias chaves de API.
    - Suporte inicial: OpenAI, Anthropic, Google Gemini, OpenRouter.
- **Modelos Locais**: Conector nativo para Ollama e LM Studio (via URL base local, ex: `http://localhost:11434`).
- **Segurança**: Chaves armazenadas de forma segura (Encrypted Local Storage ou SO Keyring).

### 3.2. Arquitetura de Projetos e Assistentes
- **Entidade Projeto**:
    - Nome, Descrição.
    - **Instruções Globais (System Prompt)**: Cada projeto atua como um "Assistente Especializado". Ex: Projeto "Jurídico" -> Prompt "Você é um advogado sênior...".
    - **Arquivos de Contexto**: Capacidade de anexar arquivos (PDF, TXT, MD) que servem de base de conhecimento para *todas* as conversas daquele projeto (RAG leve ou Contexto Longo).
- **Conversas Sem Projeto**: Suporte para chats "avulsos" que não requerem organização prévia.

### 3.3. Interface de Chat (UI/UX)
- **Barra Lateral Organizadora**:
    - **Superior**: Destaque para "Projetos" (pastas colapsáveis).
    - **Inferior**: "Chats Recentes" e "Sem Projeto" (lista cronológica).
- **Janela de Chat**:
    - Suporte total a Markdown (Code blocks, tabelas, LaTeX).
    - **Timestamps**: Exibição discreta do horário de envio/recebimento de cada mensagem.
    - Edição e bifurcação de mensagens (Branching) - *(Fase 2)*.
- **Input de Mensagem**:
    - Suporte a comandos de barra (`/`) para trocar de modelo ou persona rapidamente.

### 3.4. Gestão de Dados
- **Importação**: Ferramentas para importar dumps de dados do ChatGPT (`conversations.json`) e Claude.
- **Armazenamento**: Banco de dados Relacional Local (SQLite).
- **Backup**: Exportação completa dos dados em formato JSON/Markdown padrão.

## 4. Requisitos Não-Funcionais
- **Performance**: A interface deve carregar instantaneamente (< 200ms), mesmo com milhares de mensagens (paginação/virtualização).
- **Stack Tecnológico**:
    - Backend/Core: Python (seguindo arquitetura de 3 camadas `AGENTS_V1.0.md`).
    - Banco de Dados: SQLite.
    - Frontend (Futuro): Web Technologies (React/Next.js ou Electron/Tauri para Desktop).

## 5. Roadmap

### Fase 1: MVP (Core & CLI)
- [ ] Estrutura do Projeto e Banco de Dados (`schema.sql`).
- [ ] Scripts de Ingestão (ChatGPT/Claude Json -> SQLite).
- [ ] Scripts de Interação Básica (CLI para conversar com APIs usando o banco).

### Fase 2: UI & Contexto
- [ ] Interface Gráfica (Desktop/Web).
- [ ] Implementação da Barra Lateral (Projetos vs Chats).
- [ ] Gestão de Arquivos de Contexto por Projeto.

### Fase 3: Advanced
- [ ] Agentes Autônomos (Loop de auto-correção).
- [ ] RAG Local (Vector Database para busca semântica no histórico).
