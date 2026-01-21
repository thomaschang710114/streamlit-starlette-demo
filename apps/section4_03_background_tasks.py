import requests
import streamlit as st

st.title("3. Background Tasks")
st.caption("Non-blocking Operations")
st.markdown("""
Background tasks allow the server to return a response to the client immediately while 
continuing to process heavy work in the background.
""")

st.subheader("Live Demo")
email = st.text_input("Enter email address", "user@example.com")

if st.button("Trigger Background Task"):
    try:
        res = requests.post(
            "http://localhost:8000/api/background/email", json={"email": email}
        )
        if res.status_code == 200:
            st.success(f"✅ API responded immediately!")
            st.json(res.json())

            st.info(f"""
            **Watch your Terminal now:**
            ```text
            📧 [Background] Starting email delivery to {email}...
            (2 second delay...)
            ✅ [Background] Email sent to {email}
            ```
            """)
        else:
            st.error(f"Error: {res.status_code}")
    except Exception as e:
        st.error(f"Failed to connect: {e}")
