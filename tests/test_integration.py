import pytest
import asyncio
from pathlib import Path
from mcp_server_uv.server import UVTools, serve

async def test_project_workflow(server, mock_uv_command, temp_project_dir):
    """Test complete project workflow from init to build"""
    mock_uv_command.side_effect = [
        "Project initialized",  # init
        "Added requests to pyproject.toml",  # add
        "Lock file generated",  # lock
        "Dependencies synced",  # sync
        "Package list output",  # pip list
        "Build completed"  # build
    ]
    
    # 1. Initialize project
    result = await server.call_tool(UVTools.INIT, {
        "project_path": str(temp_project_dir),
        "name": "test-project"
    })
    assert "initialized" in result[0].text.lower()
    
    # 2. Add dependencies
    result = await server.call_tool(UVTools.ADD, {
        "project_path": str(temp_project_dir),
        "packages": ["requests"],
        "dev": False
    })
    assert "added" in result[0].text.lower()
    
    # 3. Generate lock file
    result = await server.call_tool(UVTools.LOCK, {
        "project_path": str(temp_project_dir)
    })
    assert "generated" in result[0].text.lower()
    
    # 4. Sync dependencies
    result = await server.call_tool(UVTools.SYNC, {
        "project_path": str(temp_project_dir)
    })
    assert "synced" in result[0].text.lower()
    
    # 5. List installed packages
    result = await server.call_tool(UVTools.PIP_LIST, {
        "project_path": str(temp_project_dir)
    })
    assert "output" in result[0].text.lower()
    
    # 6. Build project
    result = await server.call_tool(UVTools.BUILD, {
        "project_path": str(temp_project_dir)
    })
    assert "completed" in result[0].text.lower()

async def test_requirements_workflow(server, mock_uv_command, temp_project_dir):
    """Test requirements.txt workflow"""
    mock_uv_command.side_effect = [
        "Created requirements.txt",  # pip compile
        "Dependencies installed",    # pip sync
        "Package list output"       # pip list
    ]
    
    # 1. Compile requirements
    result = await server.call_tool(UVTools.PIP_COMPILE, {
        "project_path": str(temp_project_dir),
        "requirements_file": "requirements.txt",
        "generate_hashes": True
    })
    assert "created" in result[0].text.lower()
    
    # 2. Sync environment with requirements
    result = await server.call_tool(UVTools.PIP_SYNC, {
        "project_path": str(temp_project_dir),
        "requirements_file": "requirements.txt"
    })
    assert "installed" in result[0].text.lower()
    
    # 3. Verify installed packages
    result = await server.call_tool(UVTools.PIP_LIST, {
        "project_path": str(temp_project_dir)
    })
    assert "output" in result[0].text.lower()

async def test_error_recovery(server, mock_uv_command, temp_project_dir):
    """Test error handling and recovery in workflows"""
    mock_uv_command.side_effect = [
        "Error: Package not found",  # First install fails
        "Successfully installed",    # Second install succeeds
    ]
    
    # 1. Try installing non-existent package
    result = await server.call_tool(UVTools.PIP_INSTALL, {
        "project_path": str(temp_project_dir),
        "packages": ["nonexistent-package"]
    })
    assert "error" in result[0].text.lower()
    
    # 2. Install valid package
    result = await server.call_tool(UVTools.PIP_INSTALL, {
        "project_path": str(temp_project_dir),
        "packages": ["requests"]
    })
    assert "successfully" in result[0].text.lower()