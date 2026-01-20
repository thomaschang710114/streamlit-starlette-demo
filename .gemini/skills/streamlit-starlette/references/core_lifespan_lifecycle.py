# Capability: Lifespan for Resource Management & Cache Pre-Warming
# Use when: You need to pre-load resources (ML models, DB connections) on startup
# and clean them up on shutdown.

from contextlib import asynccontextmanager
from streamlit.starlette import App


@asynccontextmanager
async def lifespan(app):
    # --- Startup: runs BEFORE first user connects ---
    print("🚀 Starting up...")

    # Example 1: Load ML model and DB pool
    model = {"name": "placeholder_model", "loaded": True}
    db_pool = {"connection": "simulated"}

    # Example 2: Pre-warm @st.cache_data / @st.cache_resource functions
    # This ensures the first user doesn't wait for expensive computations
    # from myapp.cache import load_data, load_ml_model
    # load_data("users")       # Populates @st.cache_data
    # load_data("products")    # Populates @st.cache_data
    # load_ml_model()          # Populates @st.cache_resource

    print("✅ Ready!")

    # Yield state accessible via app.state
    yield {"model": model, "db": db_pool}

    # --- Shutdown: cleanup resources ---
    print("👋 Shutting down...")
    # db_pool.close()
    print("Resources cleaned up.")


app = App("dashboard.py", lifespan=lifespan)

# Run: uvicorn app:app --reload
