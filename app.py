import asyncio
import random
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastmcp import FastMCP
from starlette.background import BackgroundTask
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse
from starlette.responses import Response
from starlette.routing import Mount
from starlette.routing import Route
from starlette.routing import WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect
from streamlit.starlette import App

# ==============================================================================
# SECTION 1: BREAKING THE SANDBOX (Routing & Static Files)
# ==============================================================================


# 1.1 Custom API Routes (Pure Starlette)
async def custom_starlette_data(request):
    """Serve raw JSON data with minimal overhead."""
    return JSONResponse({"type": "raw_starlette", "items": [10, 20, 30]})


# 1.2 Serving Static Assets (Handled by Mount in 'routes' list)


# 1.3 SEO & Metadata Endpoints
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


# ==============================================================================
# SECTION 2: FRAMEWORK INTEROP (FastAPI & MCP)
# ==============================================================================

# 2.1 Mounting FastAPI
api = FastAPI()


@api.get("/health")
async def health():
    return {"status": "healthy", "service": "streamlit-integrated-api"}


@api.post("/predict")
async def predict(data: dict):
    return {"result": data.get("value", 0) * 2}


# 2.2 Real-time WebSockets
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    interval = float(websocket.query_params.get("interval", 1.0))
    try:
        while True:
            data = {"value": random.randint(0, 100), "ts": time.time()}
            await websocket.send_json(data)
            await asyncio.sleep(interval)
    except WebSocketDisconnect:
        print("Client disconnected")


# 2.3 MCP Server Integration
mcp = FastMCP("Streamlit Integration 🚀")


@mcp.tool
def greet(name: str) -> str:
    """Greet a user. Perfect for demoing MCP calls."""
    return f"Hello {name}! This response came from the MCP server running inside Streamlit."


mcp_app = mcp.http_app()


# ==============================================================================
# SECTION 3: PRODUCTION SECURITY & MIDDLEWARE
# ==============================================================================

ALLOWED_IPS = {"127.0.0.1", "::1"}


# 3.1 Security Headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
        return response


# 3.2 Secure Cookie Management
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


# 3.3 IP Whitelisting
class IPWhitelistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        # Allow localhost for demo
        if client_ip not in ALLOWED_IPS:
            return Response("Forbidden (IP Whitelist Demo)", status_code=403)
        return await call_next(request)


# (Helper for Demo)
async def simulate_ip_policy(request):
    ip_to_test = request.query_params.get("ip", "0.0.0.0")
    if ip_to_test in ALLOWED_IPS:
        return JSONResponse(
            {"status": "allowed", "ip": ip_to_test, "message": "Access Granted ✅"}
        )
    else:
        return JSONResponse(
            {"status": "blocked", "ip": ip_to_test, "message": "403 Forbidden ⛔"},
            status_code=403,
        )


# ==============================================================================
# SECTION 4: PERFORMANCE & LIFECYCLE
# ==============================================================================


# 4.1 Global Lifespan Resources (Simulated DB)
class FakeDBConnection:
    """Simulates a database connection pool for demo purposes."""

    async def connect(self):
        print("   ✅ [Lifespan] Database connection established")

    async def disconnect(self):
        print("   ✅ [Lifespan] Database connection closed")


db_connection = FakeDBConnection()


# 4.2 Cache Pre-warming
async def prewarm_ml_model():
    """Simulate loading a heavy ML model during startup."""
    print("   🔄 [Lifespan] Loading ML model...")
    await asyncio.sleep(0.1)
    print("   ✅ [Lifespan] ML model loaded and cached")


@asynccontextmanager
async def lifespan(app):
    print("🚀 App starting: Initializing resources...")

    # 4.1 & 4.2: Initialize resources & warm cache
    await db_connection.connect()
    await prewarm_ml_model()

    # Initialize sub-apps (MCP)
    async with mcp_app.lifespan(app):
        yield

    # Cleanup
    print("👋 App shutting down: Cleaning up resources...")
    await db_connection.disconnect()


# 4.3 Background Tasks
async def send_email_task(email: str):
    print(f"📧 [Background] Starting email delivery to {email}...")
    await asyncio.sleep(2)  # Simulate delay
    print(f"✅ [Background] Email sent to {email}")


async def background_email(request):
    data = await request.json()
    email = data.get("email", "unknown@example.com")
    task = BackgroundTask(send_email_task, email=email)
    return JSONResponse(
        {"status": "queued", "message": f"Sending email to {email}"}, background=task
    )


# ==============================================================================
# UNIFIED APP ASSEMBLY
# ==============================================================================

routes = [
    # Section 1: Custom Routes & Static
    Route("/api/raw-data", custom_starlette_data),
    Mount("/landing", app=StaticFiles(directory="landing", html=True), name="landing"),
    Route("/robots.txt", robots_txt),
    Route("/sitemap.xml", sitemap_xml),
    Route("/manifest.json", manifest_json),
    # Section 3: Security Helpers (Moved up to avoid shadowing)
    Route("/api/security/simulate-ip", simulate_ip_policy),
    # Section 4: Performance (Moved up to avoid shadowing)
    Route("/api/background/email", background_email, methods=["POST"]),
    # Section 2: Framework Interop
    Mount("/api", app=api),
    WebSocketRoute("/realtime", websocket_endpoint),
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
