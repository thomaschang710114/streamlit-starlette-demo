---
name: streamlit-starlette
description: Guidelines and patterns for integrating Streamlit with Starlette and FastAPI using the unified ASGI architecture.
---

# Streamlit-Starlette Integration Skill

This skill provides instructions and code patterns for using the `streamlit.starlette.App` wrapper, organized by architectural concern.

---

## 1. The Skeleton (Mounting & Structure)

This defines _how_ the application is structured. The primary decision is: **Who is the parent?**

### Pattern A: Streamlit as Root, FastAPI Mounted

Use when the **dashboard is the main product** and the API is a supporting feature.

**Reference**: [examples/mount_fastapi.py](examples/mount_fastapi.py)

### Pattern B: FastAPI as Root, Streamlit Mounted

Use when **FastAPI is the main product** and the dashboard is a visualization add-on.

**Reference**: [examples/mount_streamlit_as_subapp.py](examples/mount_streamlit_as_subapp.py)

### Pattern C: Custom Starlette Routes (No FastAPI)

Use when you need **simple endpoints without FastAPI overhead** (no OpenAPI docs).

**Reference**: [examples/route_custom_endpoints.py](examples/route_custom_endpoints.py)

### Pattern D: Static File Serving

Use when you need to **host a folder as a website** or serve JS/CSS assets.

**Reference**: [examples/mount_static_files.py](examples/mount_static_files.py)

### Pattern E: Django Integration

Use when integrating with an **existing Django project**.

**Reference**: [examples/mount_django.py](examples/mount_django.py)

### Pattern F: Flask Integration

Use when integrating with an **existing Flask app** (requires `a2wsgi`).

**Reference**: [examples/mount_flask.py](examples/mount_flask.py)

---

## 2. The Guard (Middleware & Security)

This defines _how_ requests are intercepted and processed before they reach the Streamlit UI.

### Pattern: Security Headers

Add security headers (CSP, X-Frame-Options, HSTS) to all responses.

**Reference**: [examples/middleware_security_headers.py](examples/middleware_security_headers.py)

### Pattern: Auth Cookie Middleware

Block access if user is not authenticated (cookie check).

**Reference**: [examples/middleware_auth.py](examples/middleware_auth.py)

### Pattern: Cookie Management

Set and read cookies via middleware.

**Reference**: [examples/middleware_cookies.py](examples/middleware_cookies.py)

### Pattern: IP Whitelist

Restrict access to specific IP addresses.

**Reference**: [examples/middleware_ip_whitelist.py](examples/middleware_ip_whitelist.py)

---

## 3. The Bridge (Communication, State & Metadata)

This defines _how_ the API layer and the UI layer share data, and how metadata is served.

### Pattern: Lifespan for Resource Management

Pre-load resources (ML models, DB pools) on startup and clean up on shutdown. Includes cache pre-warming.

**Reference**: [examples/core_lifespan_lifecycle.py](examples/core_lifespan_lifecycle.py)

### Pattern: MCP Server Integration

Expose endpoints as MCP tools for AI agents (requires `fastmcp`).

**Reference**: [examples/route_mcp_server.py](examples/route_mcp_server.py)

### Pattern: SEO Endpoints

Serve `robots.txt`, `sitemap.xml`, and `manifest.json` for SEO and PWA support.

**Reference**: [examples/route_seo_metadata.py](examples/route_seo_metadata.py)

---

## Best Practices

- **Async First**: Keep all Starlette/FastAPI route handlers `async` to avoid blocking the event loop.
- **Single Port**: The unified app runs on one port. No CORS configuration is needed between UI and API.
- **Relative Paths**: Paths to Streamlit scripts (e.g., `"dashboard.py"`) are relative to the entry point file.
