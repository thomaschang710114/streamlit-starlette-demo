# Capability: Mount Django inside Streamlit (and vice versa)
# Use when: Integrating Streamlit with an existing Django project.

# --- Option A: Django mounted inside Streamlit ---
# Streamlit at /, Django at /django/*

from starlette.routing import Mount
from django.core.asgi import get_asgi_application
from streamlit.starlette import App

django_app = get_asgi_application()

app = App(
    "dashboard.py",
    routes=[Mount("/django", app=django_app)],
)

# Run: uvicorn app:app --reload


# --- Option B: Streamlit mounted inside Django ---
# Django at /, Streamlit at /dashboard
# Place this in: myproject/asgi.py

"""
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

# Run: uvicorn myproject.asgi:application --reload
"""
