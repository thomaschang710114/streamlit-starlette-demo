import streamlit as st
import asyncio
from fastmcp import Client

st.set_page_config(page_title="MCP Client Sub-App")

st.title("🤖 MCP Client Sub-App")
st.markdown("""
This is a **separate Streamlit application** mounted at `/mcp-client`.
It uses `fastmcp.Client` to talk to the MCP server mounted at `/mcp` (in the same process!).
""")

name = st.text_input("Enter your name for the MCP greet tool", value="Ford Prefect")

client = Client("http://localhost:8000/analytics/mcp")


async def call_greet(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        return result


if st.button("Ping MCP Server"):
    with st.spinner("Calling MCP tool..."):
        try:
            result = asyncio.run(call_greet(name))
            st.success(f"Response from MCP: {result.content[0].text}")
        except Exception as e:
            st.error(f"MCP Call Failed: {e}")
