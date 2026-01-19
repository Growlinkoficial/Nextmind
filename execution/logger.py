"""
Logging utilities for NextMind.
Implements structured logging as per AGENTS_V1.0.md specification.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum


class LogLevel(Enum):
    """Log levels for the application."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class ExecutionLogger:
    """
    Structured execution logger that writes to .tmp/logs/execution_YYYYMMDD.jsonl
    
    Each log entry is a JSON object with:
    - timestamp: ISO 8601 timestamp
    - script_name: Name of the script being executed
    - inputs: Input parameters (dict)
    - outputs: Output results (dict)
    - duration_seconds: Execution time
    - status: 'success' or 'error'
    - error: Error message if status is 'error'
    """
    
    def __init__(self, log_dir: str = ".tmp/logs"):
        """
        Initialize the execution logger.
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create daily log file
        today = datetime.now().strftime("%Y%m%d")
        self.log_file = self.log_dir / f"execution_{today}.jsonl"
    
    def log(
        self,
        script_name: str,
        inputs: Dict[str, Any],
        outputs: Optional[Dict[str, Any]] = None,
        duration_seconds: Optional[float] = None,
        status: str = "success",
        error: Optional[str] = None
    ):
        """
        Log an execution entry.
        
        Args:
            script_name: Name of the script
            inputs: Input parameters
            outputs: Output results
            duration_seconds: Execution time
            status: 'success' or 'error'
            error: Error message if applicable
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "script_name": script_name,
            "inputs": inputs,
            "outputs": outputs or {},
            "duration_seconds": duration_seconds,
            "status": status,
            "error": error
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


class DecisionLogger:
    """
    Decision logger that writes to .tmp/logs/decisions_YYYYMMDD.md
    
    Documents reasoning in natural language following the template:
    ## [HH:MM:SS] Decision: [brief title]
    **Context**: [user request or trigger]
    **Options Considered**: 
    1. [Option 1]
    2. [Option 2]
    **Choice**: [selected option]
    **Reasoning**: [why this choice]
    **Risk Assessment**: [low/medium/high] - [brief explanation]
    **Scripts Called**: [list]
    """
    
    def __init__(self, log_dir: str = ".tmp/logs"):
        """
        Initialize the decision logger.
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create daily log file
        today = datetime.now().strftime("%Y%m%d")
        self.log_file = self.log_dir / f"decisions_{today}.md"
        
        # Create file with header if it doesn't exist
        if not self.log_file.exists():
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"# Decision Log - {datetime.now().strftime('%Y-%m-%d')}\n\n")
    
    def log_decision(
        self,
        title: str,
        context: str,
        options_considered: list[str],
        choice: str,
        reasoning: str,
        risk_level: str,
        risk_explanation: str,
        scripts_called: Optional[list[str]] = None
    ):
        """
        Log a decision entry.
        
        Args:
            title: Brief title of the decision
            context: User request or trigger
            options_considered: List of options that were considered
            choice: Selected option
            reasoning: Why this choice was made
            risk_level: 'low', 'medium', or 'high'
            risk_explanation: Brief explanation of the risk
            scripts_called: List of scripts that will be called
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        entry = f"""## [{timestamp}] Decision: {title}
**Context**: {context}

**Options Considered**: 
"""
        for i, option in enumerate(options_considered, 1):
            entry += f"{i}. {option}\n"
        
        entry += f"""
**Choice**: {choice}

**Reasoning**: {reasoning}

**Risk Assessment**: {risk_level} - {risk_explanation}

"""
        if scripts_called:
            entry += f"**Scripts Called**: {', '.join(scripts_called)}\n"
        
        entry += "\n---\n\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(entry)


# Convenience functions
def get_execution_logger() -> ExecutionLogger:
    """Get a singleton execution logger instance."""
    return ExecutionLogger()


def get_decision_logger() -> DecisionLogger:
    """Get a singleton decision logger instance."""
    return DecisionLogger()
