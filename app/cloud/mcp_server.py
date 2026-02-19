"""MCP Server integration for Claude Code CLI"""

# This module provides MCP Server capabilities for integration with Claude Code
# allowing direct interaction with Nanobot from Claude CLI

"""
MCP Server Tools:
- read_nanobot_memory(key: str) -> Get memory content
- add_nanobot_skill(name: str, content: str) -> Create/update skill
- list_sessions() -> List conversations
- send_telegram_message(user_id: str, msg: str) -> Send message
- get_nanobot_status() -> Health check

Usage:
    mcp connect app/cloud/mcp_server.py
"""

from pathlib import Path
import json
from typing import Any


def read_nanobot_memory(key: str = "profile") -> dict:
    """Read Nanobot memory by key"""
    memory_file = Path("./workspace/memory/MEMORY.md")
    if memory_file.exists():
        return {"content": memory_file.read_text(encoding="utf-8")}
    return {"error": "Memory not found"}


def add_nanobot_skill(name: str, content: str) -> dict:
    """Add or update a skill"""
    skill_dir = Path(f"./workspace/skills/{name}")
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(content, encoding="utf-8")
    
    return {"success": True, "skill": name}


def list_sessions(limit: int = 50) -> dict:
    """List recent sessions"""
    sessions_dir = Path("./data/sessions")
    if not sessions_dir.exists():
        return {"sessions": []}
    
    sessions = []
    for session_file in sorted(
        sessions_dir.glob("*.jsonl"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )[:limit]:
        with open(session_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    sessions.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    
    return {"sessions": sessions}


def send_telegram_message(user_id: str, msg: str) -> dict:
    """Send message via Telegram (requires bot to be running)"""
    # TODO: Implement via telegram.ext Application
    return {"sent": False, "reason": "Not implemented yet"}


def get_nanobot_status() -> dict:
    """Get current Nanobot status"""
    return {
        "status": "running",
        "version": "0.1.0",
        "environment": "cloud",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }
