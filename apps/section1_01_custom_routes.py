import requests
import streamlit as st

st.title("1. Custom API Routes")
st.caption("Bypassing FastAPI overhead")
st.markdown(
    "Fetching data from a pure Starlette `Route` (`/api/raw-data`), bypassing FastAPI overhead."
)

if st.button("Fetch Raw Data"):
    res = requests.get("http://localhost:8000/api/raw-data")
    st.json(res.json())
