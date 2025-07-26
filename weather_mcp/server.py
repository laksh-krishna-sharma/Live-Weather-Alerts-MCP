"""
Weather MCP server implementation.
"""

from mcp.server.fastmcp import FastMCP
from weather_mcp.tools import get_alerts as get_alerts_tool, get_forecast

mcp = FastMCP(
    name="weather",
    host="0.0.0.0",
    port=8000,
)


@mcp.tool(name="get_alerts")
async def _mcp_get_alerts_tool_impl(state: str) -> str:
    return await get_alerts_tool(state)


@mcp.tool(name="get_forecast")
async def get_forecast_tool(latitude: float, longitude: float) -> str:
    """Get weather forecast for given coordinates."""
    return await get_forecast(latitude, longitude)


if __name__ == "__main__":  # pragma: no cover
    TRANSPORT = "sse"
    if TRANSPORT == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif TRANSPORT == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {TRANSPORT}")
