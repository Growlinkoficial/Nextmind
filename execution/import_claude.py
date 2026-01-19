"""
Importador de conversas do Claude para o NextMind.
Lê o arquivo conversations.json exportado do Claude e insere no banco de dados.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from database import Database, Conversation, Message


def parse_claude_timestamp(timestamp_str: str) -> str:
    """
    Converte timestamp do Claude para ISO 8601.
    Claude já usa ISO 8601, então apenas valida.
    
    Args:
        timestamp_str: String de timestamp do Claude
        
    Returns:
        String ISO 8601 normalizada
    """
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.isoformat().replace('+00:00', 'Z')
    except:
        return datetime.utcnow().isoformat() + 'Z'


def import_claude_conversations(
    json_path: str,
    db: Database,
    project_id: str = None
) -> Dict[str, int]:
    """
    Importa conversas do arquivo JSON do Claude.
    
    Args:
        json_path: Caminho para conversations.json do Claude
        db: Instância do Database
        project_id: ID do projeto para vincular (opcional)
        
    Returns:
        Estatísticas da importação
    """
    print(f"Importando conversas do Claude de: {json_path}\n")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    conversation_model = Conversation(db)
    message_model = Message(db)
    
    stats = {
        'conversations_imported': 0,
        'messages_imported': 0,
        'conversations_skipped': 0
    }
    
    for chat in data:
        try:
            # Extrair informações básicas
            title = chat.get('name', 'Sem título')
            messages_data = chat.get('chat_messages', [])
            
            if not messages_data:
                stats['conversations_skipped'] += 1
                continue
            
            # Criar conversa
            conv_id = conversation_model.create(
                provider='anthropic',
                model='claude-3-opus',  # Assumindo Opus, pode ser refinado
                title=title,
                project_id=project_id
            )
            
            # Inserir mensagens
            for msg in messages_data:
                sender = msg.get('sender', 'unknown')
                
                # Mapear sender do Claude para role padrão
                if sender == 'human':
                    role = 'user'
                elif sender == 'assistant':
                    role = 'assistant'
                else:
                    role = 'system'
                
                content = msg.get('text', '')
                timestamp = parse_claude_timestamp(msg.get('created_at', ''))
                
                message_model.create(
                    conversation_id=conv_id,
                    role=role,
                    content=content,
                    meta_info=None
                )
                stats['messages_imported'] += 1
            
            stats['conversations_imported'] += 1
            print(f"✓ Importada: {title} ({len(messages_data)} mensagens)")
            
        except Exception as e:
            print(f"✗ Erro ao importar conversa: {e}")
            stats['conversations_skipped'] += 1
    
    print(f"\n=== Importação Concluída ===")
    print(f"Conversas importadas: {stats['conversations_imported']}")
    print(f"Mensagens importadas: {stats['messages_imported']}")
    print(f"Conversas ignoradas: {stats['conversations_skipped']}")
    
    return stats


if __name__ == "__main__":
    # Exemplo de uso
    db = Database()
    db.initialize_schema()
    
    # Importar conversas do Claude
    import_claude_conversations(
        json_path="chats/conversations claude.json",
        db=db,
        project_id=None  # Sem projeto (conversas avulsas)
    )
    
    db.close()
