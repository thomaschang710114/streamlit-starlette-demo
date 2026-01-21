import streamlit as st

st.title("2. Legacy Interop")
st.caption("Flask & Django")
st.markdown("""
You can mount existing WSGI applications (like Flask or Django) using `WSGIMiddleware`.

*(See `app.py` comments and `slides/code.md` for implementation details)*
""")
st.info("This section is a placeholder. While embedding Streamlit into existing legacy apps (Django/Flask) is fully supported by mounting it as a sub-app, we have chosen not to include a live demo of this specific integration in this workspace to keep the setup simple and focused on FastAPI/Starlette.")

