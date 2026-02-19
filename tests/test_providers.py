"""Tests for LLM providers"""

import pytest
from app.cloud.providers import ProviderManager


@pytest.fixture
def provider_manager():
    """Create provider manager with test settings"""
    from app.config import Settings
    import os
    
    # Use environment variables
    settings = Settings()
    return ProviderManager(settings)


def test_provider_manager_initialization(provider_manager):
    """Test provider manager initialization"""
    assert provider_manager is not None
    # At least one provider should be available
    assert (provider_manager.primary_provider is not None or 
            provider_manager.fallback_provider is not None)


def test_primary_provider_groq(provider_manager):
    """Test Groq provider initialization"""
    # Groq should be primary
    if provider_manager.primary_provider:
        assert provider_manager.primary_provider.__class__.__name__ == "GroqProvider"


def test_fallback_provider_anthropic(provider_manager):
    """Test Anthropic provider initialization"""
    # Anthropic should be fallback
    if provider_manager.fallback_provider:
        assert provider_manager.fallback_provider.__class__.__name__ == "AnthropicProvider"
