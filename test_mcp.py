import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def main():
    async with sse_client("http://127.0.0.1:9898/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.list_tools()

            print("\nRegistered MCP tools:")
            for tool in result.tools:
                print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())