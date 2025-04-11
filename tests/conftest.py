import pytest
import tempfile
import os
from pathlib import Path
from mcp.server import Server
from mcp_server_uv.server import serve

@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_uv_command(mocker):
    """Mock UV command execution"""
    return mocker.patch('mcp_server_uv.server.run_uv_command')

@pytest.fixture
async def server():
    """Create a test MCP server instance"""
    from mcp_server_uv.server import UVServer
    server = UVServer()
    await server.initialize()
    return server

@pytest.fixture
def mock_subprocess_run(mocker):
    """Mock subprocess.run for testing error scenarios"""
    return mocker.patch('subprocess.run')