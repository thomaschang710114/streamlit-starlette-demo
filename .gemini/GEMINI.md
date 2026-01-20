# Streamlit-Starlette Integration Rules

## Core Constraint

- **Unified Process**: When using the `streamlit.starlette.App` integration, NEVER run `streamlit run` and a separate FastAPI/Starlette server simultaneously. They MUST share a single ASGI process.

## Reasoning Guardrails

Before generating code, the agent MUST determine:

1.  **Mounting Direction**: Is Streamlit the root (`/`) with FastAPI mounted below, OR is FastAPI the root with Streamlit mounted at a sub-path (e.g., `/dashboard`)?
2.  **Middleware Needs**: Does the request need to be inspected/modified _before_ it reaches Streamlit? If so, use Starlette Middleware.
3.  **Lifecycle Needs**: Are there resources (DB connections, ML models) that need to be initialized on startup and cleaned up on shutdown? If so, use the `lifespan` context manager.

## Naming Conventions

- **Entry Point**: The ASGI wrapper file should be named `app.py` or `main.py`.
- **UI Script**: The Streamlit script should be named descriptively (e.g., `dashboard.py`, `streamlit_app.py`). Avoid naming it the same as the entry point.

## Execution

- **Correct**: `uvicorn app:app --reload`
- **Incorrect**: `streamlit run dashboard.py` (when using the integration)
