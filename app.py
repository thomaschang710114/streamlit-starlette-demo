from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse
from starlette.responses import Response
from starlette.routing import Mount
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from streamlit.starlette import App

# --- 1. FastAPI App ---
api = FastAPI()


@api.get("/health")
async def health():
    return {"status": "healthy", "service": "streamlit-integrated-api"}


@api.post("/predict")
async def predict(data: dict):
    return {"result": data.get("value", 0) * 2}


# --- 2. FastMCP Server ---
mcp = FastMCP("Streamlit Integration 🚀")


@mcp.tool
def greet(name: str) -> str:
    """Greet a user. Perfect for demoing MCP calls."""
    return f"Hello {name}! This response came from the MCP server running inside Streamlit."


mcp_app = mcp.http_app()


# --- 3. Custom Middleware ---
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
        return response


class CookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.set_cookie(
            key="session_id",
            value="abc123_demo",
            httponly=True,
            secure=False,  # Set to True in production
            samesite="lax",
        )
        return response


class IPWhitelistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        # Allow localhost for demo
        if client_ip not in {"127.0.0.1", "::1"}:
            return Response("Forbidden (IP Whitelist Demo)", status_code=403)
        return await call_next(request)


# --- 4. SEO & Metadata Handlers ---
async def robots_txt(request):
    return PlainTextResponse("User-agent: *\nAllow: /\nSitemap: /sitemap.xml")


async def sitemap_xml(request):
    base_url = str(request.base_url).rstrip("/")
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{base_url}/</loc>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{base_url}/static/</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>{base_url}/api/docs</loc>
    <priority>0.5</priority>
  </url>
</urlset>"""
    return Response(sitemap, media_type="application/xml")


async def manifest_json(request):
    return JSONResponse(
        {
            "name": "Streamlit Starlette Demo",
            "short_name": "SSDemo",
            "start_url": "/",
            "display": "standalone",
            "theme_color": "#ff4b4b",
        }
    )


# --- 5. Lifespan ---
@asynccontextmanager
async def lifespan(app):
    print("🚀 App starting: Pre-warming caches...")
    # FastMCP requires its lifespan to be properly initialized
    async with mcp_app.lifespan(app):
        yield
    print("👋 App shutting down...")


# --- 6. The Unified App ---
routes = [
    # SEO
    Route("/robots.txt", robots_txt),
    Route("/sitemap.xml", sitemap_xml),
    Route("/manifest.json", manifest_json),
    # Static Files (Landing Page)
    Mount("/landing", app=StaticFiles(directory="landing", html=True), name="landing"),
    # Sub-Applications
    Mount("/api", app=api),
    Mount("/analytics", app=mcp_app),
]

middleware = [
    Middleware(CookieMiddleware),
    Middleware(IPWhitelistMiddleware),
    Middleware(SecurityHeadersMiddleware),
]

app = App(
    "streamlit_app.py",
    routes=routes,
    middleware=middleware,
    lifespan=lifespan,
)
