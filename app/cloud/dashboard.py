"""Dashboard API routes for Nanobot"""

from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from app.utils import get_logger

logger = get_logger(__name__)


def create_dashboard_routes() -> APIRouter:
    """Create dashboard API routes"""
    router = APIRouter()
    
    @router.get("/sessions")
    async def get_sessions():
        """Get all sessions"""
        sessions_dir = Path("./data/sessions")
        if not sessions_dir.exists():
            return []
        
        sessions = []
        for session_file in sessions_dir.glob("*.jsonl"):
            with open(session_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        sessions.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        return sessions[-100:]  # Last 100 sessions
    
    @router.get("/memory")
    async def get_memory():
        """Get MEMORY.md content"""
        memory_file = Path("./workspace/memory/MEMORY.md")
        if memory_file.exists():
            return {"content": memory_file.read_text(encoding="utf-8")}
        return {"content": "Memory not found"}
    
    @router.post("/memory")
    async def update_memory(content: str):
        """Update MEMORY.md content"""
        memory_file = Path("./workspace/memory/MEMORY.md")
        memory_file.parent.mkdir(parents=True, exist_ok=True)
        memory_file.write_text(content, encoding="utf-8")
        logger.info("Memory updated")
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
        """Get recent logs (placeholder)"""
        return {"logs": [], "message": "Logging implemented in main.py"}
    
    return router
