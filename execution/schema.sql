-- NextMind Database Schema
-- SQLite 3.x compatible
-- Encoding: UTF-8

-- ============================================
-- TABLE: projects
-- Descrição: Projetos que agrupam conversas e definem contexto/assistentes
-- ============================================
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,  -- UUID v4
    name TEXT NOT NULL,
    description TEXT,
    global_instructions TEXT,  -- System prompt para todas as conversas deste projeto
    created_at TEXT NOT NULL DEFAULT (datetime('now')),  -- ISO 8601
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_projects_created_at ON projects(created_at DESC);

-- ============================================
-- TABLE: conversations
-- Descrição: Conversas individuais (podem ou não pertencer a um projeto)
-- ============================================
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,  -- UUID v4
    project_id TEXT,  -- FK para projects.id (NULLABLE para chats sem projeto)
    provider TEXT NOT NULL,  -- 'openai', 'anthropic', 'google', 'openrouter', 'local'
    model TEXT NOT NULL,  -- 'gpt-4', 'claude-3-opus', 'llama3-local', etc.
    title TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

CREATE INDEX idx_conversations_project_id ON conversations(project_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at DESC);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);

-- ============================================
-- TABLE: messages
-- Descrição: Mensagens individuais dentro de conversas
-- ============================================
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,  -- UUID v4
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,  -- ISO 8601 com precisão de milissegundos
    meta_info TEXT,  -- JSON opcional: {"tokens": 150, "latency_ms": 320}
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp ASC);

-- ============================================
-- TABLE: settings (Key-Value store para configurações)
-- Descrição: Armazena configurações globais (providers, theme, etc.)
-- ============================================
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,  -- JSON serializado
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Seed inicial: estrutura de providers
INSERT OR IGNORE INTO settings (key, value) VALUES 
('providers', '{"openai": {"api_key": "", "enabled": false}, "anthropic": {"api_key": "", "enabled": false}, "google": {"api_key": "", "enabled": false}, "local": {"base_url": "http://localhost:11434", "enabled": false}}');

INSERT OR IGNORE INTO settings (key, value) VALUES 
('theme', '"dark"');

-- ============================================
-- TRIGGERS: Auto-update timestamps
-- ============================================
CREATE TRIGGER IF NOT EXISTS update_projects_timestamp 
AFTER UPDATE ON projects
BEGIN
    UPDATE projects SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_conversations_timestamp 
AFTER UPDATE ON conversations
BEGIN
    UPDATE conversations SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Trigger para atualizar conversation.updated_at quando uma nova mensagem é adicionada
CREATE TRIGGER IF NOT EXISTS update_conversation_on_new_message
AFTER INSERT ON messages
BEGIN
    UPDATE conversations SET updated_at = NEW.timestamp WHERE id = NEW.conversation_id;
END;
