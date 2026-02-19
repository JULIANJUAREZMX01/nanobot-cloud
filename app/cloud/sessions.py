"""Session management - persist and load conversations"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from app.core.context import AgentContext
from app.utils import get_logger

logger = get_logger(__name__)


class SessionManager:
    """Manage conversation sessions"""

    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.sessions_dir = self.data_dir / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    async def save_session(self, ctx: AgentContext) -> bool:
        """Save session to JSONL file"""
        try:
            session_file = self.sessions_dir / f"{ctx.session_id}.jsonl"

            # Append session context as JSON line
            with open(session_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(ctx.to_dict()) + "\n")

            logger.info(f"Session saved: {ctx.session_id}")
            return True

        except Exception as e:
            logger.error(f"Error saving session: {e}")
            return False

    async def load_session(self, session_id: str) -> Optional[AgentContext]:
        """Load session from file"""
        try:
            session_file = self.sessions_dir / f"{session_id}.jsonl"

            if not session_file.exists():
                logger.info(f"No existing session: {session_id}")
                return None

            # Read last line (most recent state)
            with open(session_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if not lines:
                return None

            last_line = lines[-1].strip()
            data = json.loads(last_line)

            # Reconstruct context
            ctx = AgentContext(
                session_id=data["session_id"],
                user_id=data["user_id"],
                channel=data["channel"],
            )

            # Restore messages
            for msg_data in data.get("messages", []):
                ctx.add_message(msg_data["role"], msg_data["content"])

            logger.info(f"Session loaded: {session_id} ({len(ctx.messages)} messages)")
            return ctx

        except Exception as e:
            logger.error(f"Error loading session: {e}")
            return None

    async def list_sessions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List recent sessions"""
        try:
            sessions = []

            for session_file in sorted(
                self.sessions_dir.glob("*.jsonl"),
                key=lambda x: x.stat().st_mtime,
                reverse=True,
            )[:limit]:
                try:
                    with open(session_file, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    if lines:
                        last_line = json.loads(lines[-1])
                        sessions.append(
                            {
                                "session_id": last_line["session_id"],
                                "user_id": last_line["user_id"],
                                "channel": last_line["channel"],
                                "message_count": len(last_line.get("messages", [])),
                                "started_at": last_line["started_at"],
                            }
                        )
                except (json.JSONDecodeError, KeyError) as e:
                    logger.warning(f"Invalid session file {session_file}: {e}")

            logger.info(f"Listed {len(sessions)} sessions")
            return sessions

        except Exception as e:
            logger.error(f"Error listing sessions: {e}")
            return []

    async def cleanup_old_sessions(self, days: int = 30) -> int:
        """Delete sessions older than N days"""
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            deleted_count = 0

            for session_file in self.sessions_dir.glob("*.jsonl"):
                file_time = datetime.fromtimestamp(session_file.stat().st_mtime)

                if file_time < cutoff_time:
                    session_file.unlink()
                    deleted_count += 1
                    logger.info(f"Deleted old session: {session_file.name}")

            logger.info(f"Cleaned up {deleted_count} old sessions")
            return deleted_count

        except Exception as e:
            logger.error(f"Error cleaning up sessions: {e}")
            return 0

    async def export_session(self, session_id: str, format: str = "json") -> Optional[str]:
        """Export session to JSON or CSV"""
        try:
            session_file = self.sessions_dir / f"{session_id}.jsonl"

            if not session_file.exists():
                return None

            if format == "json":
                with open(session_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # Convert JSONL to JSON array
                sessions_data = [json.loads(line) for line in lines]
                return json.dumps(sessions_data, indent=2)

            elif format == "csv":
                import csv
                import io

                with open(session_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                sessions_data = [json.loads(line) for line in lines]

                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(["timestamp", "role", "content"])

                for session in sessions_data:
                    for msg in session.get("messages", []):
                        writer.writerow(
                            [session.get("started_at"), msg["role"], msg["content"][:100]]
                        )

                return output.getvalue()

            else:
                return None

        except Exception as e:
            logger.error(f"Error exporting session: {e}")
            return None
