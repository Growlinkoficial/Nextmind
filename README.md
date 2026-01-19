# Projeto NextMind

Este projeto foi instanciado com base na arquitetura de 3 camadas definida em `AGENTS_V1.0.md`.

## Estrutura
- `directives/`: Procedimentos Operacionais Padrão (SOPs) - Camada de Diretriz
- `execution/`: Scripts de execução (Python) - Camada de Execução
- `.tmp/`: Arquivos temporários e logs

## Banco de Dados
O NextMind utiliza SQLite para armazenamento local:
- **Schema**: `execution/schema.sql`
- **Modelos**: `execution/database.py`
- **Localização**: `.tmp/data/nextmind.db`

### Inicialização
```bash
python -c "from execution.database import Database; db = Database(); db.initialize_schema()"
```

### Importação de Dados
```bash
# ChatGPT
python execution/import_chatgpt.py

# Claude
python execution/import_claude.py
```
