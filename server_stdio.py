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
    # STDIO transport for MCP Inspector (development/debug only)
    # mcp.run(transport="stdio")
    mcp.run()