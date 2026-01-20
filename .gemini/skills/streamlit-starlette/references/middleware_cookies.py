# Capability: Cookie Middleware
# Use when: You need to set or read cookies via middleware.

from streamlit.starlette import App
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class CookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Set a session cookie (e.g., for auth persistence)
        response.set_cookie(
            key="session_id",
            value="abc123",
            httponly=True,  # Not accessible via JavaScript
            secure=True,  # Only sent over HTTPS
            samesite="lax",  # CSRF protection
            max_age=3600 * 24 * 7,  # 7 days
        )

        return response


app = App("dashboard.py", middleware=[Middleware(CookieMiddleware)])

# Run: uvicorn app:app --reload
