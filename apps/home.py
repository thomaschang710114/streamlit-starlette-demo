import streamlit as st

st.set_page_config(page_title="Streamlit-Starlette Demo", layout="wide")

st.title("🚀 Streamlit-Starlette Master Demo")

st.markdown("""
Welcome to the ultimate demonstration of the **Streamlit-Starlette** integration!

This application runs as a **single unified ASGI process**, combining the best of both worlds:
- **Streamlit**: Beautiful, interactive UI components.
- **Starlette**: Robust backend features like custom routes, middleware, and sub-app mounting.

### 🛠️ Features
1. **Custom Middleware**: Security headers, Auth cookies, and IP whitelisting.
2. **Mounted FastAPI**: REST API with OpenAPI documentation at `/api/docs`.
3. **FastMCP Server**: Exposing tools via the Model Context Protocol at `/mcp`.
4. **Static File Serving**: A Tailwind CSS landing page at `/static`.
5. **SEO Metadata**: `robots.txt`, `sitemap.xml`, and `manifest.json`.
6. **Sub-Streamlit App**: A dedicated MCP client app mounted at `/mcp-client`.
""")
