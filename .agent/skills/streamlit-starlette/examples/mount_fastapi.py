# Capability: Mount FastAPI inside Streamlit
# Use when: Dashboard is the main product, API is a supporting feature.
# Streamlit at /, FastAPI at /api/*

from fastapi import FastAPI
from starlette.routing import Mount
from streamlit.starlette import App

api = FastAPI()


@api.get("/health")
async def health():
    return {"status": "healthy"}


@api.post("/predict")
async def predict(data: dict):
    return {"prediction": data.get("value", 0) * 2}


app = App(
    "dashboard.py",
    routes=[Mount("/api", app=api)],
)

# Run: uvicorn app:app --reload
