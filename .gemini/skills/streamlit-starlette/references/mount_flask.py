# Capability: Mount Flask inside Streamlit
# Use when: Integrating Streamlit with an existing Flask app.
# Requires: pip install a2wsgi

from flask import Flask
from starlette.routing import Mount
from a2wsgi import WSGIMiddleware  # Converts WSGI to ASGI
from streamlit.starlette import App

flask_app = Flask(__name__)


@flask_app.route("/health")
def health():
    return {"status": "healthy"}


@flask_app.route("/api/legacy")
def legacy_endpoint():
    return {"message": "This is a legacy Flask endpoint"}


# Wrap Flask (WSGI) for ASGI compatibility
# Streamlit at /, Flask at /flask/*
app = App(
    "dashboard.py",
    routes=[Mount("/flask", app=WSGIMiddleware(flask_app))],
)

# Run: uvicorn app:app --reload
