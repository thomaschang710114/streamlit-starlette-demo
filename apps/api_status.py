import streamlit as st
import requests

st.title("🔗 API Status & Ping")

st.markdown("""
This page demonstrates how the Streamlit UI (Frontend) can communicate with the 
mounted FastAPI backend through internal HTTP requests.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("FastAPI Health Check")
    response = requests.get("http://localhost:8000/api/health")
    st.json(response.json())

with col2:
    st.subheader("FastAPI Random Prediction")
    val = st.number_input("Value to double", value=21)
    if st.button("Predict"):
        try:
            response = requests.post(
                "http://localhost:8000/api/predict", json={"value": val}
            )
            st.json(response.json())
        except Exception as e:
            st.error(f"Error connecting to API: {e}")

st.divider()

st.subheader("System Info (Starlette Backend)")
st.write(
    "Headers and cookies set by Starlette middleware can be inspected in the browser Network tab."
)

st.write("Streamlit can access cookies sent by the browser:")
cookies = st.context.cookies
if "session_id" in cookies:
    st.success(f"Found `session_id`: `{cookies['session_id']}`")
else:
    st.warning(
        "`session_id` not found in cookies yet. Try refreshing or checking if the middleware is correctly setting it."
    )

with st.expander("Show all cookies"):
    st.write(cookies)

st.info(
    "Note: `httponly=True` prevents Javascript access, but the server-side Streamlit app can see it via headers!"
)
