"""
Test suite for NextMind execution scripts.
Tests database operations, import functions, and logging.
"""
import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import json

from database import Database, Project, Conversation, Message
from logger import ExecutionLogger, DecisionLogger


class TestDatabase(unittest.TestCase):
    """Test database operations."""
    
    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test.db"
        self.db = Database(str(self.db_path))
        self.db.initialize_schema()
    
    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        shutil.rmtree(self.temp_dir)
    
    def test_project_creation(self):
        """Test creating a project."""
        project = Project(self.db)
        project_id = project.create(
            name="Test Project",
            description="A test project",
            global_instructions="You are a test assistant"
        )
        
        self.assertIsNotNone(project_id)
        
        # Retrieve and verify
        retrieved = project.get(project_id)
        self.assertEqual(retrieved['name'], "Test Project")
        self.assertEqual(retrieved['description'], "A test project")
    
    def test_conversation_creation(self):
        """Test creating a conversation."""
        conv = Conversation(self.db)
        conv_id = conv.create(
            provider="openai",
            model="gpt-4",
            title="Test Conversation",
            project_id=None
        )
        
        self.assertIsNotNone(conv_id)
        
        # Retrieve and verify
        retrieved = conv.get(conv_id)
        self.assertEqual(retrieved['provider'], "openai")
        self.assertEqual(retrieved['model'], "gpt-4")
        self.assertEqual(retrieved['title'], "Test Conversation")
    
    def test_message_creation(self):
        """Test creating messages in a conversation."""
        # Create conversation first
        conv = Conversation(self.db)
        conv_id = conv.create(
            provider="openai",
            model="gpt-4",
            title="Test Conversation"
        )
        
        # Create messages
        msg = Message(self.db)
        msg_id_1 = msg.create(
            conversation_id=conv_id,
            role="user",
            content="Hello, AI!"
        )
        msg_id_2 = msg.create(
            conversation_id=conv_id,
            role="assistant",
            content="Hello! How can I help you?"
        )
        
        self.assertIsNotNone(msg_id_1)
        self.assertIsNotNone(msg_id_2)
        
        # Retrieve messages
        messages = msg.list_by_conversation(conv_id)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['role'], "user")
        self.assertEqual(messages[1]['role'], "assistant")
    
    def test_project_conversation_relationship(self):
        """Test linking conversations to projects."""
        # Create project
        project = Project(self.db)
        project_id = project.create(name="Test Project")
        
        # Create conversation linked to project
        conv = Conversation(self.db)
        conv_id = conv.create(
            provider="openai",
            model="gpt-4",
            title="Project Conversation",
            project_id=project_id
        )
        
        # Retrieve conversations by project
        conversations = conv.list_by_project(project_id)
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0]['project_id'], project_id)


class TestLogging(unittest.TestCase):
    """Test logging functionality."""
    
    def setUp(self):
        """Create temporary log directory."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary log directory."""
        shutil.rmtree(self.temp_dir)
    
    def test_execution_logger(self):
        """Test execution logger creates valid JSONL."""
        logger = ExecutionLogger(log_dir=self.temp_dir)
        
        logger.log(
            script_name="test_script.py",
            inputs={"param1": "value1"},
            outputs={"result": "success"},
            duration_seconds=1.5,
            status="success"
        )
        
        # Verify log file exists
        log_files = list(Path(self.temp_dir).glob("execution_*.jsonl"))
        self.assertEqual(len(log_files), 1)
        
        # Verify log content
        with open(log_files[0], 'r', encoding='utf-8') as f:
            log_entry = json.loads(f.readline())
            self.assertEqual(log_entry['script_name'], "test_script.py")
            self.assertEqual(log_entry['status'], "success")
            self.assertEqual(log_entry['duration_seconds'], 1.5)
    
    def test_decision_logger(self):
        """Test decision logger creates valid markdown."""
        logger = DecisionLogger(log_dir=self.temp_dir)
        
        logger.log_decision(
            title="Test Decision",
            context="Testing decision logging",
            options_considered=["Option A", "Option B"],
            choice="Option A",
            reasoning="Option A is better for testing",
            risk_level="low",
            risk_explanation="This is just a test",
            scripts_called=["test_script.py"]
        )
        
        # Verify log file exists
        log_files = list(Path(self.temp_dir).glob("decisions_*.md"))
        self.assertEqual(len(log_files), 1)
        
        # Verify log content
        with open(log_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Test Decision", content)
            self.assertIn("Option A", content)
            self.assertIn("Option B", content)
            self.assertIn("test_script.py", content)


if __name__ == '__main__':
    unittest.main()
