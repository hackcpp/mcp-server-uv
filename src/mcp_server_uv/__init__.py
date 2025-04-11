import asyncio
from .server import serve

def main() -> None:
    """Entry point for the UV MCP server."""
    asyncio.run(serve())
