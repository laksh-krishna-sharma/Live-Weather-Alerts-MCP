"""
MCP client for connecting to the weather server.
"""
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()

async def get_weather_alerts(state: str = "CA") -> str:
    """
    Connects to the weather MCP server and fetches alerts for the specified state.
    """
    async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool("get_alerts", arguments={"state": state})
            return result.content[0].text
