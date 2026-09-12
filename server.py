from mcp.server.fastmcp import FastMCP

from env_loader import *
from tools import files, nlp, postgres, registry

# Create MCP instance
mcp = FastMCP("production-mcp")

# Register tools
postgres.register(mcp)
nlp.register(mcp)
registry.register(mcp)
files.register(mcp)

if __name__ == "__main__":
    mcp.settings.host = "127.0.0.1"
    mcp.settings.port = 9898
    mcp.run(transport="sse")