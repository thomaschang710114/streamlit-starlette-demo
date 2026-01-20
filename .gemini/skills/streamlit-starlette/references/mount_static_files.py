# Capability: Serve Static Files
# Use when: You need to host a folder as a website or serve JS/CSS assets.

from streamlit.starlette import App
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

app = App(
    "dashboard.py",
    routes=[
        # Serve a generated HTML site at /preview
        Mount("/preview", app=StaticFiles(directory="./static_site", html=True)),
        # Serve JS files with correct MIME types at /js
        Mount("/js", app=StaticFiles(directory="./static/js")),
        # Serve CSS files at /css
        Mount("/css", app=StaticFiles(directory="./static/css")),
    ],
)

# Run: uvicorn app:app --reload
