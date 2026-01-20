# Capability: Custom Starlette Routes
# Use when: You need simple API endpoints without FastAPI overhead.
# Lighter weight than FastAPI, no OpenAPI docs generation.

from streamlit.starlette import App
from starlette.routing import Route
from starlette.responses import JSONResponse


async def api_data(request):
    return JSONResponse({"data": [1, 2, 3]})


async def api_health(request):
    return JSONResponse({"status": "healthy"})


app = App(
    "dashboard.py",
    routes=[
        Route("/api/data", api_data),
        Route("/api/health", api_health),
    ],
)

# Run: uvicorn app:app --reload
