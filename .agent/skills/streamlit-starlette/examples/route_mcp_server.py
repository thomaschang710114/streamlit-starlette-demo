# Capability: MCP Server Integration
# Use when: You want to expose endpoints as MCP tools for AI agents.
# Requires: pip install fastmcp

from fastmcp import FastMCP
from starlette.routing import Mount
from streamlit.starlette import App

# Create FastMCP server
mcp = FastMCP("Demo 🚀")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Create ASGI app from MCP server
mcp_app = mcp.http_app()

# Mount into Streamlit - MCP available at /analytics/mcp
app = App(
    "dashboard.py",
    routes=[
        Mount("/analytics", app=mcp_app),
    ],
    lifespan=mcp_app.lifespan,
)

# Run: uvicorn app:app --reload
