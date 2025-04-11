import pytest
from mcp_server_uv.server import (
    uv_pip_list,
    uv_pip_install,
    uv_pip_uninstall,
    uv_pip_upgrade,
    uv_pip_compile,
    uv_pip_sync,
    uv_init,
    uv_add,
    uv_remove,
    uv_sync,
    uv_lock,
    uv_run,
    uv_tree,
    uv_build,
    uv_publish,
)

def test_uv_pip_list(mock_uv_command, temp_project_dir):
    """Test uv pip list command"""
    mock_uv_command.return_value = "flask==2.0.0\nrequests==2.26.0"
    
    result = uv_pip_list(str(temp_project_dir))
    
    mock_uv_command.assert_called_once_with(
        ["uv", "pip", "list", "--include-editable"],
        str(temp_project_dir)
    )
    assert "flask" in result
    assert "requests" in result

def test_uv_pip_install(mock_uv_command, temp_project_dir):
    """Test uv pip install command"""
    packages = ["requests", "flask"]
    
    # Test regular install
    uv_pip_install(str(temp_project_dir), packages)
    mock_uv_command.assert_called_with(
        ["uv", "pip", "install"] + packages,
        str(temp_project_dir)
    )
    
    # Test dev install
    uv_pip_install(str(temp_project_dir), packages, dev=True)
    mock_uv_command.assert_called_with(
        ["uv", "pip", "install", "--dev"] + packages,
        str(temp_project_dir)
    )

def test_uv_pip_uninstall(mock_uv_command, temp_project_dir):
    """Test uv pip uninstall command"""
    packages = ["requests", "flask"]
    
    uv_pip_uninstall(str(temp_project_dir), packages)
    
    mock_uv_command.assert_called_once_with(
        ["uv", "pip", "uninstall", "--yes"] + packages,
        str(temp_project_dir)
    )

def test_uv_pip_upgrade(mock_uv_command, temp_project_dir):
    """Test uv pip upgrade command"""
    # Test upgrade specific packages
    packages = ["requests", "flask"]
    uv_pip_upgrade(str(temp_project_dir), packages)
    mock_uv_command.assert_called_with(
        ["uv", "pip", "install", "--upgrade"] + packages,
        str(temp_project_dir)
    )
    
    # Test upgrade all packages
    uv_pip_upgrade(str(temp_project_dir))
    mock_uv_command.assert_called_with(
        ["uv", "pip", "install", "--upgrade", "--all"],
        str(temp_project_dir)
    )

def test_uv_pip_compile(mock_uv_command, temp_project_dir):
    """Test uv pip compile command"""
    # Test default compilation
    uv_pip_compile(str(temp_project_dir))
    mock_uv_command.assert_called_with(
        ["uv", "pip", "compile", "--generate-hashes", "requirements.txt"],
        str(temp_project_dir)
    )
    
    # Test with custom options
    uv_pip_compile(
        str(temp_project_dir),
        "dev-requirements.txt",
        upgrade=True,
        generate_hashes=False
    )
    mock_uv_command.assert_called_with(
        ["uv", "pip", "compile", "--upgrade", "dev-requirements.txt"],
        str(temp_project_dir)
    )

def test_uv_add(mock_uv_command, temp_project_dir):
    """Test uv add command"""
    packages = ["requests", "flask"]
    
    # Test regular add
    uv_add(str(temp_project_dir), packages)
    mock_uv_command.assert_called_with(
        ["uv", "add"] + packages,
        str(temp_project_dir)
    )
    
    # Test dev dependency add
    uv_add(str(temp_project_dir), packages, dev=True)
    mock_uv_command.assert_called_with(
        ["uv", "add", "--dev"] + packages,
        str(temp_project_dir)
    )

def test_uv_remove(mock_uv_command, temp_project_dir):
    """Test uv remove command"""
    packages = ["requests", "flask"]
    
    # Test regular remove
    uv_remove(str(temp_project_dir), packages)
    mock_uv_command.assert_called_with(
        ["uv", "remove"] + packages,
        str(temp_project_dir)
    )
    
    # Test dev dependency remove
    uv_remove(str(temp_project_dir), packages, dev=True)
    mock_uv_command.assert_called_with(
        ["uv", "remove", "--dev"] + packages,
        str(temp_project_dir)
    )

def test_uv_run(mock_uv_command, temp_project_dir):
    """Test uv run command"""
    command = "python -m pytest tests/"
    
    uv_run(str(temp_project_dir), command)
    
    mock_uv_command.assert_called_once_with(
        ["uv", "run", "python", "-m", "pytest", "tests/"],
        str(temp_project_dir)
    )

def test_uv_tree(mock_uv_command, temp_project_dir):
    """Test uv tree command"""
    # Test tree for all packages
    uv_tree(str(temp_project_dir))
    mock_uv_command.assert_called_with(
        ["uv", "tree"],
        str(temp_project_dir)
    )
    
    # Test tree for specific package
    uv_tree(str(temp_project_dir), "requests")
    mock_uv_command.assert_called_with(
        ["uv", "tree", "requests"],
        str(temp_project_dir)
    )

def test_other_commands(mock_uv_command, temp_project_dir):
    """Test other UV commands"""
    # Test init
    uv_init(str(temp_project_dir), "test-project")
    mock_uv_command.assert_called_with(
        ["uv", "init", "test-project"],
        str(temp_project_dir)
    )
    
    # Test sync
    uv_sync(str(temp_project_dir))
    mock_uv_command.assert_called_with(
        ["uv", "sync"],
        str(temp_project_dir)
    )
    
    # Test lock
    uv_lock(str(temp_project_dir))
    mock_uv_command.assert_called_with(
        ["uv", "lock"],
        str(temp_project_dir)
    )
    
    # Test build
    uv_build(str(temp_project_dir))
    mock_uv_command.assert_called_with(
        ["uv", "build"],
        str(temp_project_dir)
    )
    
    # Test publish
    uv_publish(str(temp_project_dir), "testpypi")
    mock_uv_command.assert_called_with(
        ["uv", "publish", "--repository", "testpypi"],
        str(temp_project_dir)
    )