"""Tool execution for agent - shell, files, git, web"""

import asyncio
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlparse

from app.utils import get_logger

logger = get_logger(__name__)

# Safe paths - restrict to user's development directory
SAFE_BASE_PATHS = [
    Path("C:/Users/QUINTANA/sistemas"),
]


class ToolExecutor:
    """Execute tools safely"""

    async def execute(self, tool_call: Dict[str, Any]) -> str:
        """Execute tool call"""
        name = tool_call.get("name", "unknown")
        args = tool_call.get("args", {})

        try:
            logger.info(f"Executing tool: {name}")

            if name == "execute_shell":
                return await self._execute_shell(args)
            elif name == "read_file":
                return await self._read_file(args)
            elif name == "write_file":
                return await self._write_file(args)
            elif name == "git_operation":
                return await self._git_operation(args)
            elif name == "web_fetch":
                return await self._web_fetch(args)
            else:
                return f"❌ Herramienta desconocida: {name}"

        except Exception as e:
            logger.error(f"Tool error ({name}): {e}")
            return f"❌ Error en {name}: {str(e)[:200]}"

    async def _execute_shell(self, args: Dict[str, Any]) -> str:
        """Execute shell command safely"""
        command = args.get("command", "").strip()

        if not command:
            return "❌ Comando vacío"

        # Safety check - block dangerous commands
        dangerous = ["rm -rf", "dd if=", "format", "shutdown", "reboot"]
        if any(d in command for d in dangerous):
            return "❌ Comando peligroso bloqueado"

        try:
            logger.info(f"Executing: {command[:100]}")

            result = await asyncio.to_thread(
                subprocess.run,
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )

            output = result.stdout if result.returncode == 0 else result.stderr
            return output.strip()[:2000]  # Limit output

        except subprocess.TimeoutExpired:
            return "❌ Comando excedió timeout (30s)"
        except Exception as e:
            return f"❌ Error ejecutando comando: {str(e)}"

    async def _read_file(self, args: Dict[str, Any]) -> str:
        """Read file safely"""
        path = args.get("path", "").strip()

        if not path:
            return "❌ Ruta vacía"

        try:
            file_path = Path(path).resolve()

            # Security check
            if not self._is_safe_path(file_path):
                return f"❌ Acceso denegado: fuera de directorio permitido"

            if not file_path.exists():
                return f"❌ Archivo no existe: {path}"

            if file_path.is_dir():
                return f"❌ Es directorio, no archivo: {path}"

            content = await asyncio.to_thread(file_path.read_text, encoding="utf-8")
            return content[:5000]  # Limit output

        except Exception as e:
            return f"❌ Error leyendo {path}: {str(e)}"

    async def _write_file(self, args: Dict[str, Any]) -> str:
        """Write file safely"""
        path = args.get("path", "").strip()
        content = args.get("content", "")

        if not path:
            return "❌ Ruta vacía"

        try:
            file_path = Path(path).resolve()

            # Security check
            if not self._is_safe_path(file_path):
                return f"❌ Acceso denegado: fuera de directorio permitido"

            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)

            await asyncio.to_thread(file_path.write_text, content, encoding="utf-8")
            return f"✅ Archivo escrito: {path} ({len(content)} bytes)"

        except Exception as e:
            return f"❌ Error escribiendo {path}: {str(e)}"

    async def _git_operation(self, args: Dict[str, Any]) -> str:
        """Execute git operation safely"""
        operation = args.get("operation", "").strip()
        repo_path = args.get("repo_path", "C:/Users/QUINTANA/sistemas").strip()

        if not operation:
            return "❌ Operación vacía"

        # Only allow safe git operations
        safe_ops = ["status", "log", "branch", "diff", "show", "pull", "add", "commit"]
        if not any(op in operation.lower() for op in safe_ops):
            return "❌ Operación git no permitida"

        try:
            logger.info(f"Git: {operation}")

            result = await asyncio.to_thread(
                subprocess.run,
                f'cd "{repo_path}" && git {operation}',
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )

            output = result.stdout if result.returncode == 0 else result.stderr
            return output.strip()[:2000]

        except subprocess.TimeoutExpired:
            return "❌ Comando git excedió timeout"
        except Exception as e:
            return f"❌ Error git: {str(e)}"

    async def _web_fetch(self, args: Dict[str, Any]) -> str:
        """Fetch web content safely"""
        url = args.get("url", "").strip()

        if not url:
            return "❌ URL vacía"

        try:
            # Parse URL for security
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return "❌ URL inválida"

            import httpx

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url, follow_redirects=True)
                return response.text[:3000]

        except Exception as e:
            return f"❌ Error fetching {url}: {str(e)}"

    @staticmethod
    def _is_safe_path(path: Path) -> bool:
        """Check if path is in safe directories"""
        try:
            path = path.resolve()
            for safe_base in SAFE_BASE_PATHS:
                safe_base = safe_base.resolve()
                if str(path).startswith(str(safe_base)):
                    return True
            return False
        except Exception:
            return False
