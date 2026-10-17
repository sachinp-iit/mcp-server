from mcp.server.fastmcp import FastMCP

from env_loader import *
from tools import files, nlp, postgres, rag, registry

mcp = FastMCP("rag-mcp-server")

# Register existing tools.
postgres.register(mcp)
nlp.register(mcp)
registry.register(mcp)
files.register(mcp)

# Register transcript RAG tools.
rag.register(mcp)

if __name__ == "__main__":
    mcp.run(transport="sse")