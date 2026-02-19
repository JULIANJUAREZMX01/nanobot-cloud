"""Tests for Phase 2: Agent Loop + LLM Integration"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

from app.core.loop import AgentLoop
from app.core.context import AgentContext
from app.core.tools import ToolExecutor
from app.cloud.providers import ProviderManager
from app.cloud.sessions import SessionManager
from app.config import Settings


@pytest.fixture
def settings():
    """Test settings"""
    return Settings(
        telegram_token="test_token",
        groq_api_key="test_groq",
        anthropic_api_key="test_anthropic",
        environment="test"
    )


@pytest.fixture
async def provider_manager(settings):
    """Test provider manager"""
    # Mock the API clients to avoid actual API calls
    with patch("app.cloud.providers.groq.Groq"), \
         patch("app.cloud.providers.anthropic.Anthropic"):
        return ProviderManager(settings)


@pytest.fixture
async def agent_loop(settings, provider_manager):
    """Test agent loop"""
    return AgentLoop(settings, provider_manager)


@pytest.fixture
def context():
    """Test context"""
    ctx = AgentContext(
        session_id="test_session",
        user_id="test_user",
        channel="test"
    )
    return ctx


@pytest.mark.asyncio
async def test_agent_loop_initialization(agent_loop):
    """Test agent loop initializes correctly"""
    assert agent_loop is not None
    assert agent_loop.tool_executor is not None


@pytest.mark.asyncio
async def test_context_message_addition(context):
    """Test adding messages to context"""
    context.add_message("user", "Hello")
    assert len(context.messages) == 1
    assert context.messages[0].role == "user"
    assert context.messages[0].content == "Hello"


@pytest.mark.asyncio
async def test_context_to_dict(context):
    """Test context serialization"""
    context.add_message("user", "Test")
    data = context.to_dict()
    
    assert data["session_id"] == "test_session"
    assert data["user_id"] == "test_user"
    assert len(data["messages"]) == 1


@pytest.mark.asyncio
async def test_tool_executor_initialization():
    """Test tool executor initializes"""
    executor = ToolExecutor()
    assert executor is not None


@pytest.mark.asyncio
async def test_tool_executor_safe_path():
    """Test tool executor safe path checking"""
    from pathlib import Path
    executor = ToolExecutor()
    
    # Safe path
    safe = executor._is_safe_path(Path("C:/Users/QUINTANA/sistemas/test"))
    assert safe is True
    
    # Unsafe path
    unsafe = executor._is_safe_path(Path("C:/Windows/System32"))
    assert unsafe is False


@pytest.mark.asyncio
async def test_session_manager_initialization():
    """Test session manager initializes"""
    manager = SessionManager()
    assert manager is not None
    assert manager.sessions_dir.exists()


@pytest.mark.asyncio
async def test_session_manager_save_and_load(context):
    """Test saving and loading sessions"""
    manager = SessionManager()
    
    # Save
    success = await manager.save_session(context)
    assert success is True
    
    # Load
    loaded = await manager.load_session(context.session_id)
    assert loaded is not None
    assert loaded.session_id == context.session_id
    assert loaded.user_id == context.user_id


@pytest.mark.asyncio
async def test_session_manager_list_sessions(context):
    """Test listing sessions"""
    manager = SessionManager()
    
    # Save a session
    await manager.save_session(context)
    
    # List
    sessions = await manager.list_sessions()
    assert len(sessions) > 0
    assert sessions[0]["session_id"] == context.session_id


@pytest.mark.asyncio
async def test_agent_loop_format_messages(agent_loop, context):
    """Test message formatting for LLM"""
    context.add_message("user", "Hello")
    messages = agent_loop._format_messages(context)
    
    # Should have system + user message
    assert len(messages) >= 1
    assert messages[0]["role"] == "system"


@pytest.mark.asyncio
async def test_agent_loop_build_system_prompt(agent_loop, context):
    """Test system prompt building"""
    prompt = agent_loop._build_system_prompt(context)
    
    assert "Nanobot" in prompt
    assert "QUINTANA" in prompt
    assert "español" in prompt.lower()


@pytest.mark.asyncio
async def test_tool_executor_execute_shell():
    """Test shell command execution"""
    executor = ToolExecutor()
    
    # Safe command
    result = await executor._execute_shell({"command": "echo test"})
    assert "test" in result
    
    # Dangerous command
    result = await executor._execute_shell({"command": "rm -rf /"})
    assert "bloqueado" in result.lower()


@pytest.mark.asyncio
async def test_tool_executor_read_file(tmp_path):
    """Test file reading"""
    executor = ToolExecutor()
    
    # Create temp file in safe path
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")
    
    # Should fail because path is not safe
    result = await executor._read_file({"path": str(test_file)})
    assert "acceso denegado" in result.lower()


@pytest.mark.asyncio
async def test_provider_manager_initialization(settings):
    """Test provider manager initializes"""
    with patch("app.cloud.providers.groq.Groq"), \
         patch("app.cloud.providers.anthropic.Anthropic"):
        manager = ProviderManager(settings)
        assert manager is not None


@pytest.mark.asyncio
async def test_provider_manager_get_provider(provider_manager):
    """Test getting provider"""
    provider = provider_manager.get_provider()
    assert provider is not None
    assert hasattr(provider, "call")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
