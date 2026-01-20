# Capability: Mount Streamlit inside FastAPI
# Use when: FastAPI is the main product, Streamlit is a visualization add-on.
# FastAPI at /, Streamlit at /dashboard

from fastapi import FastAPI
from streamlit.starlette import App

streamlit_app = App("dashboard.py")
api = FastAPI(lifespan=streamlit_app.lifespan())


@api.get("/api/status")
async def status():
    return {"status": "ok"}


@api.get("/api/data")
async def get_data():
    return {"data": [1, 2, 3]}


api.mount("/dashboard", streamlit_app)

# Run: uvicorn app:api --reload
