"""LLM Provider management - Groq primary, Anthropic fallback"""

import asyncio
from typing import List, Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import Settings
from app.utils import get_logger

logger = get_logger(__name__)


class GroqProvider:
    """Groq LLM provider (primary)"""

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        from groq import Groq
        self.client = Groq(api_key=api_key)
        self.model = model
        self.name = "groq"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def call(
        self, messages: List[Dict[str, str]], max_tokens: int = 8192, temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Call Groq API"""
        try:
            logger.info(f"Calling Groq ({self.model})")

            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            content = response.choices[0].message.content
            logger.info(f"Groq response: {len(content)} chars")

            return {"text": content, "tool_calls": []}

        except Exception as e:
            logger.error(f"Groq error: {e}")
            raise


class AnthropicProvider:
    """Anthropic Claude provider (fallback)"""

    def __init__(self, api_key: str, model: str = "claude-opus-4-5"):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.name = "anthropic"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def call(
        self, messages: List[Dict[str, str]], max_tokens: int = 8192, temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Call Anthropic API"""
        try:
            logger.info(f"Calling Anthropic ({self.model})")

            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages,
            )

            content = response.content[0].text
            logger.info(f"Anthropic response: {len(content)} chars")

            return {"text": content, "tool_calls": []}

        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            raise


class ProviderManager:
    """Manage LLM providers with fallback logic"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.groq_provider = None
        self.anthropic_provider = None
        self._init_providers()

    def _init_providers(self):
        """Initialize providers"""
        try:
            if self.settings.groq_api_key:
                self.groq_provider = GroqProvider(self.settings.groq_api_key)
                logger.info("✅ Groq provider initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Groq: {e}")

        try:
            if self.settings.anthropic_api_key:
                self.anthropic_provider = AnthropicProvider(self.settings.anthropic_api_key)
                logger.info("✅ Anthropic provider initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Anthropic: {e}")

        if not self.groq_provider and not self.anthropic_provider:
            logger.error("❌ No LLM providers available!")

    def get_provider(self):
        """Get provider (Groq first, fallback to Anthropic)"""
        if self.groq_provider:
            return self.groq_provider
        if self.anthropic_provider:
            logger.warning("⚠️  Groq unavailable, using Anthropic fallback")
            return self.anthropic_provider
        raise RuntimeError("No LLM providers available")

    async def call(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 8192,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """Call LLM with fallback logic"""
        provider = self.get_provider()

        try:
            return await provider.call(messages, max_tokens, temperature)
        except Exception as e:
            logger.error(f"{provider.name} failed: {e}")

            # Try fallback
            if provider.name == "groq" and self.anthropic_provider:
                logger.info("Trying Anthropic fallback...")
                try:
                    return await self.anthropic_provider.call(messages, max_tokens, temperature)
                except Exception as fallback_err:
                    logger.error(f"Anthropic fallback also failed: {fallback_err}")
                    raise

            raise
