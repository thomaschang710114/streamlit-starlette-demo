# Capability: IP Whitelist Middleware
# Use when: You need to restrict access to specific IP addresses.

from streamlit.starlette import App
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Define allowed IPs (extend with CIDR ranges if needed)
ALLOWED_IPS = {
    "127.0.0.1",
    "192.168.1.100",
    "10.0.0.1",
}


class IPWhitelistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        client_ip = request.client.host

        if client_ip not in ALLOWED_IPS:
            return Response("Forbidden", status_code=403)

        return await call_next(request)


app = App("dashboard.py", middleware=[Middleware(IPWhitelistMiddleware)])

# Run: uvicorn app:app --reload
