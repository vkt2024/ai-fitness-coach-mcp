import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


class MCPToolAdapter:
    def __init__(self, url="http://localhost:8000/sse"):
        self.url = url

    async def call_tool(self, tool_name: str, arguments: dict):
        async with sse_client(self.url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content


def call_mcp_tool_sync(tool_name: str, arguments: dict):
    adapter = MCPToolAdapter()
    return asyncio.run(adapter.call_tool(tool_name, arguments))