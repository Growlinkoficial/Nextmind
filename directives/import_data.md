---
priority: high
domain: data_processing
dependencies: [database_management]
conflicts_with: []
last_updated: 2026-01-19
---

# Diretiva: Importação de Dados de Conversas

## Objetivo
Importar conversas históricas de provedores de IA (ChatGPT, Claude) para o banco de dados NextMind, preservando metadados e estrutura.

## Inputs Necessários
- Arquivo JSON de exportação do ChatGPT (`conversations.json`)
- Arquivo JSON de exportação do Claude (`conversations.json`)
- ID do projeto (opcional) para vincular conversas importadas
- Banco de dados inicializado

## Scripts de Execução

### 1. Importação ChatGPT
**Script**: `execution/import_chatgpt.py`
**Função**: `import_chatgpt_conversations(json_path, db, project_id)`

**Características**:
- Lineariza estrutura em árvore (mapping) do ChatGPT
- Segue caminho principal (primeiro filho em cada nó)
- Ignora branches laterais (conversas bifurcadas)
- Preserva timestamps originais

**Uso**:
```python
from execution.database import Database
from execution.import_chatgpt import import_chatgpt_conversations

db = Database()
db.initialize_schema()

stats = import_chatgpt_conversations(
    json_path="chats/conversations gpt.json",
    db=db,
    project_id=None  # Ou UUID de projeto específico
)
```

### 2. Importação Claude
**Script**: `execution/import_claude.py`
**Função**: `import_claude_conversations(json_path, db, project_id)`

**Características**:
- Estrutura já é linear (chat_messages)
- Mapeia roles: 'human' → 'user', 'assistant' → 'assistant'
- Preserva timestamps e metadados

**Uso**:
```python
from execution.database import Database
from execution.import_claude import import_claude_conversations

db = Database()
stats = import_claude_conversations(
    json_path="chats/conversations claude.json",
    db=db,
    project_id=None
)
```

## Outputs Esperados
- Conversas inseridas na tabela `conversations`
- Mensagens inseridas na tabela `messages`
- Estatísticas de importação (dict):
  - `conversations_imported`: Número de conversas importadas com sucesso
  - `messages_imported`: Total de mensagens importadas
  - `conversations_skipped`: Conversas ignoradas (vazias ou com erro)

## Critérios de Sucesso
- Todas as conversas válidas importadas sem erros
- Timestamps preservados corretamente (ISO 8601 UTC)
- Integridade referencial mantida (conversation_id válido em todas as mensagens)
- Encoding UTF-8 correto (emojis e caracteres especiais)
- Conversas sem projeto (project_id NULL) funcionam corretamente

## Edge Cases Conhecidos

### 1. Conversas Vazias (ChatGPT)
- **Problema**: Algumas conversas têm mapping vazio ou sem mensagens válidas
- **Solução**: Ignorar e incrementar `conversations_skipped`
- **Impacto**: Normal, não indica erro

### 2. Timestamps Inválidos
- **Problema**: Timestamps malformados, None ou 0
- **Solução**: Usar `datetime.utcnow()` como fallback
- **Impacto**: Mensagem terá timestamp de importação ao invés de original

### 3. Caracteres Especiais e Emojis
- **Problema**: Emojis, Unicode e caracteres especiais em mensagens
- **Solução**: Garantir encoding UTF-8 em todas as operações de leitura/escrita
- **Impacto**: Resolvido no código, não requer ação manual

### 4. Estrutura em Árvore (ChatGPT)
- **Problema**: ChatGPT permite bifurcações (múltiplas respostas alternativas)
- **Solução**: Seguir apenas o primeiro filho em cada nó (caminho principal)
- **Impacto**: Branches laterais são perdidos na importação

### 5. Conversas Muito Grandes
- **Problema**: Conversas com milhares de mensagens podem ser lentas
- **Solução**: Importação é feita em transações por conversa
- **Impacto**: Performance aceitável, ~5-10s para 100 conversas

## Tempo de Execução Estimado
- ChatGPT (100 conversas): ~5-10s
- Claude (100 conversas): ~3-5s
- Depende do número de mensagens por conversa

## Validação Pós-Importação

Após importação, verificar:

```python
from execution.database import Conversation, Message

# Contar conversas importadas
conv = Conversation(db)
all_convs = conv.list_by_project(None)
print(f"Total de conversas sem projeto: {len(all_convs)}")

# Verificar mensagens de uma conversa
msg = Message(db)
messages = msg.list_by_conversation(all_convs[0]['id'])
print(f"Primeira conversa tem {len(messages)} mensagens")
```

## Troubleshooting

### Erro: "No such file or directory"
- Verificar se o arquivo JSON existe no caminho especificado
- Usar caminho absoluto ou relativo correto

### Erro: "JSONDecodeError"
- Arquivo JSON corrompido ou formato inválido
- Validar JSON com ferramenta externa (jq, jsonlint)

### Erro: "UNIQUE constraint failed"
- Tentativa de reimportar mesmas conversas
- Limpar banco antes de reimportar ou usar IDs únicos

### Importação lenta
- Normal para grandes volumes
- Considerar importação em batches se necessário
