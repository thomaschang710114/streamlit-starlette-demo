import requests
import streamlit as st

st.title("1. Custom API Routes")
st.caption("Bypassing FastAPI overhead with pure Starlette routes")

# --- 1.1a JSON Response ---
st.subheader("📦 JSON Response")
st.markdown("Fetch raw JSON data from `/api/raw-data`.")

if st.button("Fetch Raw Data", key="json"):
    res = requests.get("http://localhost:8000/api/raw-data")
    st.json(res.json())

st.divider()

# --- 1.1b HTML Response ---
st.subheader("🎨 HTML Response")
st.markdown("Fetch styled HTML from `/api/html-demo` and render with `st.html()`.")

if st.button("Fetch HTML", key="html"):
    res = requests.get("http://localhost:8000/api/html-demo")
    st.html(res.text)

st.divider()

# --- 1.1c Plain Text Response ---
st.subheader("📝 Plain Text Response")
st.markdown("Fetch plain text from `/api/plain-text`.")

if st.button("Fetch Plain Text", key="plaintext"):
    res = requests.get("http://localhost:8000/api/plain-text")
    st.code(res.text, language=None)

st.divider()

# --- 1.1d Redirect Response ---
st.subheader("🔀 Redirect Response")
st.markdown(
    "Clicking the link below will trigger a **303 redirect** to my newsletter."
)
st.link_button("Test Redirect →", "http://localhost:8000/api/redirect-demo")

st.divider()

# --- 1.1e Path Parameters ---
st.subheader("🔗 Path Parameters")
st.markdown("Starlette routes can extract dynamic segments from the URL.")

col1, col2 = st.columns(2)
with col1:
    user_id = st.text_input("User ID", value="42", key="user_id")
with col2:
    action = st.text_input("Action (optional)", value="profile", key="action")

if st.button("Fetch with Path Params", key="params"):
    if action:
        url = f"http://localhost:8000/api/users/{user_id}/{action}"
    else:
        url = f"http://localhost:8000/api/users/{user_id}"
    
    st.caption(f"Calling: `{url}`")
    res = requests.get(url)
    st.json(res.json())
