# Adding custom routes

```python
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
```

# Adding custom middleware

```python
from streamlit.starlette import App
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response

app = App(
    "main.py",
    middleware=[Middleware(SecurityHeadersMiddleware)],
)
```

# Mounting FastAPI in Streamlit

```python
from fastapi import FastAPI
from starlette.routing import Mount
from streamlit.starlette import App

# Create FastAPI sub-application
api = FastAPI()

@api.get("/health")
async def health():
    return {"status": "healthy"}

@api.post("/predict")
async def predict(data: dict):
    return {"prediction": data.get("value", 0) * 2}

# Mount FastAPI into Streamlit app
# - Streamlit UI at /
# - FastAPI endpoints at /api/*
# - FastAPI docs at /api/docs
app = App(
    "dashboard.py",
    routes=[Mount("/api", app=api)],
)
```

# Mounting Streamlit in FastAPI

```python
from fastapi import FastAPI
from streamlit.starlette import App

# Create the Streamlit sub-application
streamlit_app = App("dashboard.py")

# Create FastAPI with Streamlit's lifespan to manage the runtime lifecycle
api = FastAPI(lifespan=streamlit_app.lifespan())

@api.get("/api/data")
async def get_data():
    return {"data": [1, 2, 3]}

# Mount Streamlit under /dashboard
api.mount("/dashboard", streamlit_app)

# Run with: uvicorn myapp:api
```

# Lifespan hooks for startup/shutdown

```python
from contextlib import asynccontextmanager
from streamlit.starlette import App

@asynccontextmanager
async def lifespan(app):
    # Startup: runs before accepting connections
    print("🚀 Starting up...")
    model = load_ml_model()  # Pre-warm caches
    db = init_db_connection()

    # Yield state accessible via app.state
    yield {"model": model, "db": db}

    # Shutdown: cleanup resources
    print("👋 Shutting down...")
    db.close()

app = App("main.py", lifespan=lifespan)
```

# You can now add REST API endpoints alongside your Streamlit app:

```python
from streamlit.starlette import App
from starlette.routing import Route
from starlette.responses import JSONResponse

async def api_data(request):
    return JSONResponse({"data": [1, 2, 3]})

async def api_health(request):
    return JSONResponse({"status": "healthy"})

app = App(
    "main.py",
    routes=[
        Route("/api/data", api_data),
        Route("/api/health", api_health),
    ],
)
```

# You can also mount a full FastAPI app for more features (OpenAPI docs, Pydantic validation, etc.):

```python
from fastapi import FastAPI
from starlette.routing import Mount
from streamlit.starlette import App

api = FastAPI()

@api.get("/health")
async def health():
    return {"status": "healthy"}

@api.post("/predict")
async def predict(data: dict):
    return {"result": data.get("value", 0) * 2}

# Streamlit at /, FastAPI at /api/*, OpenAPI docs at /api/docs
app = App("main.py", routes=[Mount("/api", app=api)])
```

# You can now serve robots.txt at the root level:

```python
from streamlit.starlette import App
from starlette.routing import Route
from starlette.responses import PlainTextResponse

async def robots_txt(request):
    return PlainTextResponse(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
    )

app = App("main.py", routes=[Route("/robots.txt", robots_txt)])
```

# You can now host a folder as a static website alongside your Streamlit app:

```python
from streamlit.starlette import App
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

# Serve generated site folder at /preview
app = App(
    "main.py",
    routes=[
        Mount("/preview", app=StaticFiles(directory="./static_site", html=True)),
    ],
)
```

# You can serve JavaScript files (and other static assets) with correct content types:

```python
from streamlit.starlette import App
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

# Serve JS files from a directory with correct MIME types
app = App(
    "main.py",
    routes=[
        Mount("/js", app=StaticFiles(directory="./static/js")),
    ],
)
```

# Custom MCP endpoint:

```python
from streamlit.starlette import App
from starlette.routing import Route
from starlette.responses import JSONResponse

async def mcp_handler(request):
    body = await request.json()
    # Handle MCP protocol messages here
    return JSONResponse({"result": "..."})

app = App("main.py", routes=[Route("/mcp", mcp_handler, methods=["POST"])])
```

# Using MCP libraries like FastMCP:

```python
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
```

# You can now add security headers to all responses:

```python
from streamlit.starlette import App
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response

app = App("main.py", middleware=[Middleware(SecurityHeadersMiddleware)])
```

# You can now set cookies in responses

```python
from streamlit.starlette import App
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

class CookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # Set a cookie (e.g., for auth persistence)
        response.set_cookie(
            key="session_id",
            value="abc123",
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600 * 24 * 7,  # 7 days
        )
        return response

app = App("main.py", middleware=[Middleware(CookieMiddleware)])
```

# You can now implement IP whitelisting:

```python
from streamlit.starlette import App
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

ALLOWED_IPS = {"127.0.0.1", "192.168.1.100", "10.0.0.0/8"}

class IPWhitelistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        if client_ip not in ALLOWED_IPS:
            return Response("Forbidden", status_code=403)
        return await call_next(request)

app = App("main.py", middleware=[Middleware(IPWhitelistMiddleware)])
```

# You can now run Streamlit as a standard ASGI application:

```python
from streamlit.starlette import App

app = App("dashboard.py")

# Run with any ASGI server:
# uvicorn myapp:app
# gunicorn -k uvicorn.workers.UvicornWorker myapp:app
# hypercorn myapp:app
# or streamlit run myapp.py
```

# This also enables deploying Streamlit alongside Django, FastAPI, Flask or other frameworks:

```python
from starlette.routing import Mount
from django.core.asgi import get_asgi_application
from streamlit.starlette import App

django_app = get_asgi_application()

# Mount Django into Streamlit
# Streamlit at /, Django at /django/*
app = App(
    "dashboard.py",
    routes=[Mount("/django", app=django_app)],
)
```

# Mount Flask inside Streamlit:

```python
from flask import Flask
from starlette.routing import Mount
from a2wsgi import WSGIMiddleware  # pip install a2wsgi
from streamlit.starlette import App

flask_app = Flask(__name__)

@flask_app.route("/health")
def health():
    return {"status": "healthy"}

# Wrap Flask (WSGI) for ASGI compatibility
app = App("dashboard.py", routes=[Mount("/flask", app=WSGIMiddleware(flask_app))])
```

# You can now mount Streamlit as an ASGI sub-application within Django:

```python
# myproject/asgi.py, run with uvicorn myproject.asgi:application
from django.core.asgi import get_asgi_application
from starlette.routing import Mount
from starlette.applications import Starlette
from streamlit.starlette import App

django_app = get_asgi_application()
streamlit_app = App("analytics/dashboard.py")

application = Starlette(routes=[
    Mount("/dashboard", app=streamlit_app),
    Mount("/", app=django_app),
])
```

# You can now run startup code (like cache pre-warming) before accepting connections:

```python
from contextlib import asynccontextmanager
from streamlit.starlette import App

@asynccontextmanager
async def lifespan(app):
    # Startup: runs BEFORE first user connects
    print("🚀 Pre-warming caches...")

    # Call your @st.cache_resource functions here
    from myapp.cache import load_ml_model, init_db_pool
    load_ml_model()   # Populates cache
    init_db_pool()    # Ready for connections

    print("✅ Ready!")
    yield

    print("👋 Shutting down...")

app = App("main.py", lifespan=lifespan)
```

# You can now pre-warm caches at startup before the first user connects:

```python
from contextlib import asynccontextmanager
from streamlit.starlette import App

@asynccontextmanager
async def lifespan(app):
    print("🚀 Pre-caching data...")

    # Call cached functions to populate cache
    from myapp import load_data, compute_stats
    load_data("users")      # @st.cache_data
    load_data("products")   # @st.cache_data
    compute_stats()         # @st.cache_resource

    print("✅ Cache warmed!")
    yield

    # Run any close operations here

app = App("main.py", lifespan=lifespan)
```

# You can now run initialization code outside the script runner, before any Streamlit script executes:

```python
from contextlib import asynccontextmanager
from streamlit.starlette import App

@asynccontextmanager
async def lifespan(app):
    # Setup: runs ONCE at server start, outside script runner
    print("🚀 Running setup...")

    import os
    os.environ["MY_CONFIG"] = "production"

    # Initialize shared resources
    from myapp import setup_logging, init_services
    setup_logging()
    init_services()

    yield

    # Teardown
    print("👋 Cleanup...")

app = App("main.py", lifespan=lifespan)
```

# You can now serve custom metadata files like manifest.json:

```python
from streamlit.starlette import App
from starlette.routing import Route
from starlette.responses import JSONResponse

async def manifest(request):
    return JSONResponse({
        "name": "My Analytics App",
        "short_name": "Analytics",
        "description": "Interactive data dashboard",
        "icons": [{"src": "/app/static/icon-192.png", "sizes": "192x192"}],
        "theme_color": "#ff4b4b",
        "background_color": "#ffffff",
    })

app = App("main.py", routes=[Route("/manifest.json", manifest)])
```

# You can now serve SEO metadata endpoints for crawlers:

```python
from streamlit.starlette import App
from starlette.routing import Route
from starlette.responses import PlainTextResponse, Response

async def robots_txt(request):
    return PlainTextResponse("User-agent: *\nAllow: /\nSitemap: /sitemap.xml")

async def sitemap_xml(request):
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://myapp.com/</loc></url>
  <url><loc>https://myapp.com/dashboard</loc></url>
</urlset>'''
    return Response(sitemap, media_type="application/xml")

app = App(
    "main.py",
    routes=[
        Route("/robots.txt", robots_txt),
        Route("/sitemap.xml", sitemap_xml),
    ],
)
```
