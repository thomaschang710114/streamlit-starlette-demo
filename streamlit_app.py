import streamlit as st

# Common sidebar elements
with st.sidebar:
    st.markdown("### 🌐 Starlette Endpoints")
    st.caption("These are served directly by Starlette/FastAPI:")
    st.link_button("Landing Page", "/landing/", use_container_width=True)
    st.link_button("FastAPI Docs", "/api/docs", use_container_width=True)

    st.divider()
    st.markdown("### 📄 Metadata")

    st.link_button("Robots", "http://localhost:8000/robots.txt", width="stretch")
    st.link_button("Sitemap", "http://localhost:8000/sitemap.xml", width="stretch")
    st.link_button("Manifest", "http://localhost:8000/manifest.json", width="stretch")

# Define pages for Multipage v2
home_page = st.Page("apps/home.py", title="Home", icon="🏠", default=True)
api_page = st.Page("apps/api_status.py", title="API Status", icon="🔗")
mcp_client_page = st.Page("apps/mcp_client.py", title="MCP Client", icon="🤖")

# Navigation setup
pg = st.navigation([home_page, api_page, mcp_client_page])

# Run navigation
pg.run()
