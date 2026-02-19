"""Main agent loop - processes messages and executes tools"""

import asyncio
import json
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.config import Settings
from app.utils import get_logger
from app.core.context import AgentContext, Message
from app.core.tools import ToolExecutor
from app.cloud.providers import ProviderManager

logger = get_logger(__name__)


class AgentLoop:
    """Main agent loop for processing user messages"""

    def __init__(self, settings: Settings, provider_manager: ProviderManager):
        self.settings = settings
        self.provider_manager = provider_manager
        self.tool_executor = ToolExecutor()

    async def process_message(self, ctx: AgentContext) -> str:
        """
        Process user message and generate response
        
        Args:
            ctx: AgentContext with user message
            
        Returns:
            Response text
        """
        try:
            # Get LLM provider
            provider = self.provider_manager.get_provider()
            logger.info(f"Using provider: {provider.__class__.__name__}")

            # Prepare messages for LLM
            messages = self._format_messages(ctx)

            # Call LLM
            logger.info(f"Calling LLM with {len(messages)} messages")
            llm_response = await provider.call(messages)

            # Parse response
            response_text = llm_response.get("text", "")
            tool_calls = llm_response.get("tool_calls", [])

            # Execute tools if needed
            if tool_calls:
                logger.info(f"Executing {len(tool_calls)} tool calls")
                for tool_call in tool_calls:
                    tool_result = await self.tool_executor.execute(tool_call)
                    ctx.add_message("tool", tool_result, metadata={"tool": tool_call.get("name")})

            # Add assistant response
            ctx.add_message("assistant", response_text)
            logger.info("Message processed successfully")

            return response_text

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            error_msg = f"Disculpa, ocurrió un error: {str(e)[:100]}"
            ctx.add_message("assistant", error_msg, metadata={"error": True})
            return error_msg

    def _format_messages(self, ctx: AgentContext) -> List[Dict[str, str]]:
        """Format context messages for LLM API"""
        formatted = []

        # Add system prompt
        system_prompt = self._build_system_prompt(ctx)
        formatted.append({"role": "system", "content": system_prompt})

        # Add conversation history
        for msg in ctx.messages:
            formatted.append({"role": msg.role, "content": msg.content})

        return formatted

    def _build_system_prompt(self, ctx: AgentContext) -> str:
        """Build system prompt with context information"""
        prompt = """Eres Nanobot, asistente personal de desarrollo de QUINTANA (Julian Juarez).

## Tu Rol
- Senior developer assistant
- Especialista en: Python, JavaScript, DevOps, cloud deployment
- Acceso a herramientas: shell, files, git, web

## Comunicación
- Siempre en español
- Breve y al grano (máximo 4 líneas salvo que pida detalle)
- Técnico y directo
- Muestra output real de comandos

## Herramientas Disponibles
Puedes usar:
- execute_shell(command) → output
- read_file(path) → content
- write_file(path, content)
- git_operation(cmd)
- web_fetch(url)

Llama herramientas cuando sea necesario para ayudar."""

        # Add user context if available
        if hasattr(ctx, 'user_id'):
            prompt += f"\n\nUsuario: {ctx.user_id}"
        if hasattr(ctx, 'channel'):
            prompt += f"\nCanal: {ctx.channel}"

        return prompt

    async def handle_tool_response(self, tool_response: str, ctx: AgentContext) -> str:
        """Handle tool response and generate follow-up"""
        try:
            # Add tool response to context
            ctx.add_message("tool", tool_response)

            # Get provider and call LLM again
            provider = self.provider_manager.get_provider()
            messages = self._format_messages(ctx)

            llm_response = await provider.call(messages)
            response_text = llm_response.get("text", "")

            ctx.add_message("assistant", response_text)
            return response_text

        except Exception as e:
            logger.error(f"Error handling tool response: {e}")
            return f"Error procesando respuesta de herramienta: {str(e)[:100]}"
