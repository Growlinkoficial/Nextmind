"""
Script de teste para validar o schema do banco de dados NextMind.
Cria dados de exemplo e verifica as relações.
"""
from database import Database, Project, Conversation, Message
import json


def main():
    print("=== NextMind Database Test ===\n")
    
    # 1. Inicializar banco de dados
    print("1. Inicializando banco de dados...")
    db = Database(".tmp/data/nextmind_test.db")
    db.initialize_schema()
    print("   ✓ Schema criado com sucesso\n")
    
    # 2. Criar modelos
    project_model = Project(db)
    conversation_model = Conversation(db)
    message_model = Message(db)
    
    # 3. Criar um projeto
    print("2. Criando projeto 'Desenvolvimento Python'...")
    project_id = project_model.create(
        name="Desenvolvimento Python",
        description="Projeto para auxiliar em desenvolvimento Python",
        global_instructions="Você é um especialista em Python. Responda de forma concisa e técnica."
    )
    print(f"   ✓ Projeto criado: {project_id}\n")
    
    # 4. Criar conversa vinculada ao projeto
    print("3. Criando conversa vinculada ao projeto...")
    conv_id = conversation_model.create(
        provider="openai",
        model="gpt-4",
        title="Como usar decorators em Python",
        project_id=project_id
    )
    print(f"   ✓ Conversa criada: {conv_id}\n")
    
    # 5. Criar conversa SEM projeto
    print("4. Criando conversa sem projeto...")
    conv_no_project_id = conversation_model.create(
        provider="local",
        model="llama3-local",
        title="Chat rápido sobre clima",
        project_id=None
    )
    print(f"   ✓ Conversa sem projeto criada: {conv_no_project_id}\n")
    
    # 6. Adicionar mensagens à primeira conversa
    print("5. Adicionando mensagens com timestamps...")
    msg1_id = message_model.create(
        conversation_id=conv_id,
        role="user",
        content="O que são decorators em Python?"
    )
    
    msg2_id = message_model.create(
        conversation_id=conv_id,
        role="assistant",
        content="Decorators são funções que modificam o comportamento de outras funções...",
        meta_info={"tokens": 45, "latency_ms": 320}
    )
    
    msg3_id = message_model.create(
        conversation_id=conv_id,
        role="user",
        content="Pode dar um exemplo prático?"
    )
    print(f"   ✓ 3 mensagens criadas\n")
    
    # 7. Validar dados
    print("6. Validando dados inseridos...\n")
    
    # Buscar projeto
    project = project_model.get(project_id)
    print(f"   Projeto: {project['name']}")
    print(f"   Instruções: {project['global_instructions'][:50]}...\n")
    
    # Listar conversas do projeto
    project_convs = conversation_model.list_by_project(project_id)
    print(f"   Conversas no projeto: {len(project_convs)}")
    for conv in project_convs:
        print(f"     - {conv['title']} ({conv['provider']}/{conv['model']})")
    
    # Listar conversas sem projeto
    no_project_convs = conversation_model.list_by_project(None)
    print(f"\n   Conversas sem projeto: {len(no_project_convs)}")
    for conv in no_project_convs:
        print(f"     - {conv['title']} ({conv['provider']}/{conv['model']})")
    
    # Listar mensagens da primeira conversa
    messages = message_model.list_by_conversation(conv_id)
    print(f"\n   Mensagens na conversa '{project_convs[0]['title']}':")
    for msg in messages:
        print(f"     [{msg['timestamp']}] {msg['role']}: {msg['content'][:50]}...")
        if msg['meta_info']:
            meta = json.loads(msg['meta_info'])
            print(f"       Meta: {meta}")
    
    print("\n=== Teste concluído com sucesso! ===")
    
    db.close()


if __name__ == "__main__":
    main()
