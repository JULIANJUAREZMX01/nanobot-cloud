"""Tests for tool executor"""

import pytest
from pathlib import Path
from app.core.tools import ToolExecutor
from app.core.context import AgentContext


@pytest.fixture
def tool_executor(tmp_path):
    """Create tool executor with temporary workspace"""
    executor = ToolExecutor(str(tmp_path))
    return executor


@pytest.fixture
def agent_context():
    """Create test agent context"""
    ctx = AgentContext(
        session_id="test_session",
        user_id="test_user",
        channel="test"
    )
    return ctx


@pytest.mark.asyncio
async def test_tool_executor_initialization(tool_executor):
    """Test tool executor initialization"""
    assert tool_executor is not None
    assert "execute_shell" in tool_executor.tools
    assert "read_file" in tool_executor.tools
    assert "write_file" in tool_executor.tools


@pytest.mark.asyncio
async def test_read_file_not_found(tool_executor, agent_context):
    """Test reading non-existent file"""
    result = await tool_executor.read_file(
        {"path": "nonexistent.txt"},
        agent_context
    )
    assert "not found" in result.lower()


@pytest.mark.asyncio
async def test_write_and_read_file(tool_executor, agent_context, tmp_path):
    """Test writing and reading a file"""
    # Write file
    write_result = await tool_executor.write_file(
        {"path": "test.txt", "content": "Hello, World!"},
        agent_context
    )
    assert "written" in write_result.lower()
    
    # Read file
    read_result = await tool_executor.read_file(
        {"path": "test.txt"},
        agent_context
    )
    assert "Hello, World!" in read_result


@pytest.mark.asyncio
async def test_list_files_empty(tool_executor, agent_context):
    """Test listing empty directory"""
    result = await tool_executor.list_files(
        {"directory": "."},
        agent_context
    )
    assert "empty" in result.lower() or result == ""


@pytest.mark.asyncio
async def test_tool_not_found(tool_executor, agent_context):
    """Test calling non-existent tool"""
    result = await tool_executor.execute(
        "nonexistent_tool",
        {},
        agent_context
    )
    assert "not found" in result.lower()
