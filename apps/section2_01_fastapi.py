import requests
import streamlit as st

st.header("1. FastAPI Mounting")
st.markdown("Interacting with the mounted FastAPI sub-application (`/api`).")

st.subheader("Health Check")
if st.button("Check Health"):
    response = requests.get("http://localhost:8000/api/health")
    st.json(response.json())

st.subheader("Prediction API")
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
st.link_button(
    "📖 Open FastAPI Swagger Docs (/api/docs)",
    "/api/docs",
    use_container_width=True,
)

st.warning(
    "**Note:** While it's possible to embed Streamlit into legacy apps (Django/Flask) by mounting it as a sub-app, we have chosen not to demo that specific integration here to keep the focus on FastAPI/Starlette."
)
