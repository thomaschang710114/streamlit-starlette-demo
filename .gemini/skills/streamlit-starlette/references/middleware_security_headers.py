# Capability: Security Headers Middleware
# Use when: You need to add security headers to all responses.

from streamlit.starlette import App
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


app = App("dashboard.py", middleware=[Middleware(SecurityHeadersMiddleware)])

# Run: uvicorn app:app --reload
