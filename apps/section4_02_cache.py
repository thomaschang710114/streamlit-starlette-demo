import streamlit as st

st.title("2. Cache Pre-warming")
st.caption("Eliminating Cold Starts")
st.markdown("""
By loading heavy resources (like ML models) during the lifespan startup, we eliminate the 
"cold start" delay for the first user who visits the dashboard.
""")

st.info("""
**Expected Terminal Output on Startup:**
```text
🔄 [Lifespan] Loading ML model...
✅ [Lifespan] ML model loaded and cached
```
""")
