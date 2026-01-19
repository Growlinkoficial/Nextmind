"""
NextMind Database Models
Modelos Python para interação com o banco de dados SQLite.
"""
import sqlite3
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
import json


class Database:
    """Gerenciador de conexão com o banco de dados SQLite."""
    
    def __init__(self, db_path: str = ".tmp/data/nextmind.db"):
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados SQLite
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: Optional[sqlite3.Connection] = None
        
    def connect(self) -> sqlite3.Connection:
        """Estabelece conexão com o banco de dados."""
        if self.conn is None:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
        return self.conn
    
    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def initialize_schema(self, schema_path: str = "execution/schema.sql"):
        """
        Inicializa o schema do banco de dados.
        
        Args:
            schema_path: Caminho para o arquivo schema.sql
        """
        conn = self.connect()
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        conn.commit()


class Project:
    """Modelo para a entidade Project."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create(
        self,
        name: str,
        description: Optional[str] = None,
        global_instructions: Optional[str] = None
    ) -> str:
        """
        Cria um novo projeto.
        
        Args:
            name: Nome do projeto
            description: Descrição opcional
            global_instructions: System prompt para o assistente
            
        Returns:
            UUID do projeto criado
        """
        project_id = str(uuid.uuid4())
        conn = self.db.connect()
        conn.execute(
            """
            INSERT INTO projects (id, name, description, global_instructions)
            VALUES (?, ?, ?, ?)
            """,
            (project_id, name, description, global_instructions)
        )
        conn.commit()
        return project_id
    
    def get(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Busca um projeto por ID."""
        conn = self.db.connect()
        row = conn.execute(
            "SELECT * FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
        return dict(row) if row else None
    
    def list_all(self) -> List[Dict[str, Any]]:
        """Lista todos os projetos ordenados por data de criação."""
        conn = self.db.connect()
        rows = conn.execute(
            "SELECT * FROM projects ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


class Conversation:
    """Modelo para a entidade Conversation."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create(
        self,
        provider: str,
        model: str,
        title: str,
        project_id: Optional[str] = None
    ) -> str:
        """
        Cria uma nova conversa.
        
        Args:
            provider: Nome do provedor ('openai', 'anthropic', etc.)
            model: Nome do modelo
            title: Título da conversa
            project_id: ID do projeto (opcional)
            
        Returns:
            UUID da conversa criada
        """
        conversation_id = str(uuid.uuid4())
        conn = self.db.connect()
        conn.execute(
            """
            INSERT INTO conversations (id, project_id, provider, model, title)
            VALUES (?, ?, ?, ?, ?)
            """,
            (conversation_id, project_id, provider, model, title)
        )
        conn.commit()
        return conversation_id
    
    def get(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Busca uma conversa por ID."""
        conn = self.db.connect()
        row = conn.execute(
            "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
        ).fetchone()
        return dict(row) if row else None
    
    def list_by_project(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Lista conversas de um projeto específico ou sem projeto.
        
        Args:
            project_id: ID do projeto (None para conversas sem projeto)
        """
        conn = self.db.connect()
        if project_id is None:
            rows = conn.execute(
                "SELECT * FROM conversations WHERE project_id IS NULL ORDER BY updated_at DESC"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM conversations WHERE project_id = ? ORDER BY updated_at DESC",
                (project_id,)
            ).fetchall()
        return [dict(row) for row in rows]


class Message:
    """Modelo para a entidade Message."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create(
        self,
        conversation_id: str,
        role: str,
        content: str,
        meta_info: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Cria uma nova mensagem.
        
        Args:
            conversation_id: ID da conversa
            role: 'user', 'assistant', ou 'system'
            content: Conteúdo da mensagem
            meta_info: Metadados opcionais (tokens, latência, etc.)
            
        Returns:
            UUID da mensagem criada
        """
        message_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        meta_json = json.dumps(meta_info) if meta_info else None
        
        conn = self.db.connect()
        conn.execute(
            """
            INSERT INTO messages (id, conversation_id, role, content, timestamp, meta_info)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (message_id, conversation_id, role, content, timestamp, meta_json)
        )
        conn.commit()
        return message_id
    
    def list_by_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Lista todas as mensagens de uma conversa ordenadas por timestamp."""
        conn = self.db.connect()
        rows = conn.execute(
            "SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
            (conversation_id,)
        ).fetchall()
        return [dict(row) for row in rows]
