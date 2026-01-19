---
priority: high
domain: data_management
dependencies: []
conflicts_with: []
last_updated: 2026-01-19
---

# Diretiva: Gerenciamento do Banco de Dados NextMind

## Objetivo
Manter e operar o banco de dados SQLite do NextMind, incluindo inicialização, importação de dados, e consultas.

## Inputs Necessários
- Arquivo `schema.sql` (para inicialização)
- Arquivos JSON de backup (ChatGPT, Claude) para importação
- Credenciais/configurações (armazenadas em `settings` table)

## Scripts de Execução

### 1. Inicialização do Banco
**Script**: `execution/database.py`
**Função**: `Database.initialize_schema()`
**Uso**:
```python
from database import Database
db = Database(".tmp/data/nextmind.db")
db.initialize_schema()
```

### 2. Importação de Dados

#### ChatGPT
**Script**: `execution/import_chatgpt.py`
**Função**: `import_chatgpt_conversations(json_path, db, project_id)`
**Notas**:
- Lineariza estrutura em árvore (mapping)
- Segue caminho principal (primeiro filho)
- Ignora branches laterais

#### Claude
**Script**: `execution/import_claude.py`
**Função**: `import_claude_conversations(json_path, db, project_id)`
**Notas**:
- Estrutura já é linear (chat_messages)
- Mapeia 'human' -> 'user', 'assistant' -> 'assistant'

### 3. Operações CRUD

#### Projetos
```python
from database import Project
project = Project(db)
project_id = project.create(name="Meu Projeto", global_instructions="...")
```

#### Conversas
```python
from database import Conversation
conv = Conversation(db)
conv_id = conv.create(provider="openai", model="gpt-4", title="...", project_id=None)
```

#### Mensagens
```python
from database import Message
msg = Message(db)
msg.create(conversation_id=conv_id, role="user", content="...")
```

## Outputs Esperados
- Banco de dados SQLite em `.tmp/data/nextmind.db`
- Logs de importação (stdout)
- Estatísticas de importação (dict)

## Critérios de Sucesso
- Schema criado sem erros
- Dados importados com integridade referencial
- Timestamps preservados corretamente
- Conversas sem projeto (project_id NULL) funcionam

## Edge Cases Conhecidos

### 1. Conversas Vazias no ChatGPT
- **Problema**: Algumas conversas têm mapping vazio
- **Solução**: Ignorar e incrementar `conversations_skipped`

### 2. Timestamps Inválidos
- **Problema**: Timestamps malformados ou ausentes
- **Solução**: Usar `datetime.utcnow()` como fallback

### 3. Caracteres Especiais
- **Problema**: Emojis e Unicode em mensagens
- **Solução**: Usar encoding UTF-8 em todas as operações

## Tempo de Execução Estimado
- Inicialização: < 1s
- Importação ChatGPT (100 conversas): ~5-10s
- Importação Claude (100 conversas): ~3-5s

## Manutenção
- Backup regular: Copiar `.tmp/data/nextmind.db` para local seguro
- Limpeza: Deletar `.tmp/data/nextmind_test.db` após testes
