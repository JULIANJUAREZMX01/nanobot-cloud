"""Dashboard API routes for Nanobot"""

from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
import os
from app.utils import get_logger

logger = get_logger(__name__)


def create_dashboard_routes() -> APIRouter:
    """Create dashboard API routes"""
    router = APIRouter()
    
    @router.get("/sessions")
    async def get_sessions():
        """Get all sessions"""
        # Use plural and specific directory
        sessions_dir = Path("./data/sessions")
        if not sessions_dir.exists():
            return []
        
        sessions = []
        # Check for both .json and .jsonl
        for session_file in list(sessions_dir.glob("*.json")) + list(sessions_dir.glob("*.jsonl")):
            try:
                # If it's a small JSON file, read it directly
                content = session_file.read_text(encoding="utf-8")
                if session_file.suffix == ".jsonl":
                    # Read the last line of JSONL for current state
                    lines = content.strip().split('\n')
                    data = json.loads(lines[-1])
                else:
                    data = json.loads(content)
                
                # Add file info
                data["session_id"] = session_file.stem
                data["last_modified"] = os.path.getmtime(session_file)
                sessions.append(data)
            except Exception as e:
                logger.error(f"Error reading session {session_file}: {e}")
                continue
        
        # Sort by last modified
        sessions.sort(key=lambda x: x.get("last_modified", 0), reverse=True)
        return sessions[:50]
    
    @router.get("/memory")
    async def get_memory():
        """Get MEMORY.md content"""
        memory_file = Path("./workspace/memory/MEMORY.md")
        if memory_file.exists():
            return {"content": memory_file.read_text(encoding="utf-8")}
        return {"content": "# Memory not found\n\nThe memory file hasn't been created yet."}
    
    @router.post("/memory")
    async def update_memory(data: dict):
        """Update MEMORY.md content"""
        content = data.get("content", "")
        memory_file = Path("./workspace/memory/MEMORY.md")
        memory_file.parent.mkdir(parents=True, exist_ok=True)
        memory_file.write_text(content, encoding="utf-8")
        logger.info("Memory updated via dashboard")
        return {"success": True}
    
    @router.get("/skills")
    async def get_skills():
        """List available skills"""
        skills_dir = Path("./workspace/skills")
        if not skills_dir.exists():
            return []
        
        skills = []
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    skills.append({
                        "name": skill_dir.name,
                        "content": skill_md.read_text(encoding="utf-8")
                    })
        
        return skills
    
    @router.get("/logs")
    async def get_logs(limit: int = 50):
        """Get recent logs from standard logger (simple version)"""
        # This is a placeholder for a real log file reader
        # Since we use loguru/standard logger, we would need to read from a file
        return {"logs": ["Logs system ready", "Checking for activity..."], "message": "Real-time logs can be seen in Render Dashboard"}
    
    return router
