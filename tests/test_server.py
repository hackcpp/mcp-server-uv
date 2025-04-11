import pytest
from pathlib import Path
from mcp.types import TextContent
from mcp_server_uv.server import UVTools

async def test_list_tools(server):
    """Test tool list functionality"""
    tools = await server.list_tools()
    
    assert len(tools) > 0
    tool_names = [tool.name for tool in tools]
    
    # Verify all UV tools are present
    assert UVTools.PIP_LIST in tool_names
    assert UVTools.PIP_INSTALL in tool_names
    assert UVTools.PIP_UNINSTALL in tool_names
    assert UVTools.PIP_UPGRADE in tool_names
    assert UVTools.ADD in tool_names
    assert UVTools.REMOVE in tool_names
    
    # Verify tool schemas
    pip_install_tool = next(t for t in tools if t.name == UVTools.PIP_INSTALL)
    schema = pip_install_tool.inputSchema
    assert "project_path" in schema["properties"]
    assert "packages" in schema["properties"]
    assert "dev" in schema["properties"]

async def test_call_tool_pip_list(server, mock_uv_command, temp_project_dir):
    """Test pip list tool execution"""
    mock_uv_command.return_value = "flask==2.0.0\nrequests==2.26.0"
    
    result = await server.call_tool(UVTools.PIP_LIST, {
        "project_path": str(temp_project_dir)
    })
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "flask" in result[0].text
    assert "requests" in result[0].text

async def test_call_tool_pip_install(server, mock_uv_command, temp_project_dir):
    """Test pip install tool execution"""
    mock_uv_command.return_value = "Successfully installed flask-2.0.0"
    
    result = await server.call_tool(UVTools.PIP_INSTALL, {
        "project_path": str(temp_project_dir),
        "packages": ["flask"],
        "dev": True
    })
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert "Successfully installed" in result[0].text

async def test_call_tool_error_handling(server, mock_uv_command, temp_project_dir):
    """Test error handling in tool execution"""
    mock_uv_command.return_value = "Error: Package not found"
    
    result = await server.call_tool(UVTools.PIP_INSTALL, {
        "project_path": str(temp_project_dir),
        "packages": ["nonexistent-package"]
    })
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert "Error" in result[0].text

async def test_call_tool_invalid_tool(server):
    """Test handling of invalid tool names"""
    with pytest.raises(ValueError, match="Unknown tool"):
        await server.call_tool("invalid_tool", {
            "project_path": "/tmp"
        })

async def test_call_tool_init_project(server, mock_uv_command, temp_project_dir):
    """Test project initialization"""
    mock_uv_command.return_value = "Project initialized successfully"
    
    result = await server.call_tool(UVTools.INIT, {
        "project_path": str(temp_project_dir),
        "name": "test-project"
    })
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert "initialized" in result[0].text.lower()