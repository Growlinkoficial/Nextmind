"""
Importador de conversas do ChatGPT para o NextMind.
Lê o arquivo conversations.json exportado do ChatGPT e insere no banco de dados.
"""
import json
import uuid
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from database import Database, Conversation, Message
from logger import get_execution_logger


def parse_chatgpt_timestamp(timestamp: float) -> str:
    """
    Converte timestamp Unix do ChatGPT para ISO 8601.
    
    Args:
        timestamp: Unix timestamp (segundos desde epoch)
        
    Returns:
        String ISO 8601 (UTC)
    """
    return datetime.utcfromtimestamp(timestamp).isoformat() + 'Z'


def linearize_conversation(mapping: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Lineariza a estrutura em árvore do ChatGPT em uma lista ordenada.
    Segue o caminho principal (primeiro filho) ignorando branches.
    
    Args:
        mapping: Dicionário de nós do ChatGPT
        
    Returns:
        Lista de mensagens ordenadas cronologicamente
    """
    messages = []
    
    # Encontrar o nó raiz (sem parent)
    root_id = None
    for node_id, node in mapping.items():
        if node.get('parent') is None:
            root_id = node_id
            break
    
    if not root_id:
        return messages
    
    # Percorrer a árvore seguindo o primeiro filho
    current_id = root_id
    while current_id:
        node = mapping.get(current_id)
        if not node:
            break
        
        message_data = node.get('message')
        if message_data and message_data.get('content'):
            content_parts = message_data['content'].get('parts', [])
            if content_parts:
                messages.append({
                    'role': message_data['author']['role'],
                    'content': '\n'.join(content_parts),
                    'timestamp': message_data.get('create_time', 0)
                })
        
        # Seguir para o primeiro filho
        children = node.get('children', [])
        current_id = children[0] if children else None
    
    return messages


def import_chatgpt_conversations(
    json_path: str,
    db: Database,
    project_id: str = None
) -> Dict[str, int]:
    """
    Importa conversas do arquivo JSON do ChatGPT.
    
    Args:
        json_path: Caminho para conversations.json
        db: Instância do Database
        project_id: ID do projeto para vincular (opcional)
        
    Returns:
        Estatísticas da importação
    """
    logger = get_execution_logger()
    start_time = time.time()
    
    print(f"Importando conversas do ChatGPT de: {json_path}\n")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        duration = time.time() - start_time
        logger.log(
            script_name="import_chatgpt.py",
            inputs={"json_path": json_path, "project_id": project_id},
            outputs={},
            duration_seconds=duration,
            status="error",
            error=f"Failed to read JSON file: {str(e)}"
        )
        raise
    
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
            title = chat.get('title', 'Sem título')
            mapping = chat.get('mapping', {})
            
            # Linearizar mensagens
            messages = linearize_conversation(mapping)
            
            if not messages:
                stats['conversations_skipped'] += 1
                continue
            
            # Criar conversa
            conv_id = conversation_model.create(
                provider='openai',
                model='gpt-4',  # Assumindo GPT-4, pode ser refinado
                title=title,
                project_id=project_id
            )
            
            # Inserir mensagens
            for msg in messages:
                message_model.create(
                    conversation_id=conv_id,
                    role=msg['role'],
                    content=msg['content'],
                    meta_info=None
                )
                stats['messages_imported'] += 1
            
            stats['conversations_imported'] += 1
            print(f"✓ Importada: {title} ({len(messages)} mensagens)")
            
        except Exception as e:
            print(f"✗ Erro ao importar conversa: {e}")
            stats['conversations_skipped'] += 1
    
    duration = time.time() - start_time
    
    print(f"\n=== Importação Concluída ===")
    print(f"Conversas importadas: {stats['conversations_imported']}")
    print(f"Mensagens importadas: {stats['messages_imported']}")
    print(f"Conversas ignoradas: {stats['conversations_skipped']}")
    
    # Log execution
    logger.log(
        script_name="import_chatgpt.py",
        inputs={"json_path": json_path, "project_id": project_id},
        outputs=stats,
        duration_seconds=duration,
        status="success"
    )
    
    return stats


if __name__ == "__main__":
    # Exemplo de uso
    db = Database()
    db.initialize_schema()
    
    # Importar conversas do ChatGPT
    import_chatgpt_conversations(
        json_path="chats/conversations gpt.json",
        db=db,
        project_id=None  # Sem projeto (conversas avulsas)
    )
    
    db.close()
