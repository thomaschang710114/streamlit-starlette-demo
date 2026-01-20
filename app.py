from streamlit.starlette import App
from starlette.routing import Route
from starlette.responses import JSONResponse


async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "streamlit-app"})


async def get_data(request):
    return JSONResponse({"items": ["apple", "banana", "cherry"], "count": 3})


app = App(
    "main.py",
    routes=[
        Route("/api/health", health_check),
        Route("/api/data", get_data),
    ],
)
