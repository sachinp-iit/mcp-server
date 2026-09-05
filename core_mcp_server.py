import asyncio

from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

# Create an instance of Original MCP Server and we give name as "core-mcp-server"
server = Server("core-mcp-server")

async def main():
    # MCP Server uses standard protocol runtime which is STDIO
    async with stdio_server() as (read_stream, write_stream):
        print("Core-MCP-Server Started...")
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )

# Starting the async thread and calling main method in that thread
if __name__ == "__main__":
    asyncio.run(main())