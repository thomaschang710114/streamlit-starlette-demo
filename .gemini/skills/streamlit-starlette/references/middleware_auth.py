# Capability: Auth Cookie Middleware
# Use when: You need to block access to Streamlit if the user is not authenticated.

from streamlit.starlette import App
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Allow health checks and static assets
        if request.url.path.startswith("/_stcore"):
            return await call_next(request)

        # Check for session token
        if "session_token" not in request.cookies:
            return RedirectResponse(url="/login", status_code=303)

        return await call_next(request)


app = App("dashboard.py", middleware=[Middleware(AuthMiddleware)])

# Run: uvicorn app:app --reload
