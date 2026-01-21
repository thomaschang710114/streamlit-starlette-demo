import streamlit as st

st.title("1. Global Lifespan Resources")
st.caption("Startup/Shutdown Events")
st.markdown("""
Resources like database connection pools are initialized once when the server starts and 
cleaned up when it shuts down.
""")

st.info("""
**Expected Terminal Output on Startup:**
```text
🚀 App starting: Initializing resources...
✅ [Lifespan] Database connection established
```
""")
