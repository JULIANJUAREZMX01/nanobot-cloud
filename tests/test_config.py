"""Tests for configuration"""

import os
import pytest
from app.config import Settings


def test_settings_from_env():
    """Test settings loading from environment"""
    os.environ["TELEGRAM_TOKEN"] = "test_token"
    os.environ["GROQ_API_KEY"] = "test_groq"
    os.environ["ANTHROPIC_API_KEY"] = "test_anthropic"
    
    settings = Settings()
    assert settings.telegram_token == "test_token"
    assert settings.groq_api_key == "test_groq"
    assert settings.anthropic_api_key == "test_anthropic"


def test_settings_defaults():
    """Test default settings"""
    os.environ["TELEGRAM_TOKEN"] = "token"
    os.environ["GROQ_API_KEY"] = "groq"
    os.environ["ANTHROPIC_API_KEY"] = "anthropic"
    
    settings = Settings()
    assert settings.environment == "development"
    assert settings.port == 8000
    assert settings.host == "0.0.0.0"
