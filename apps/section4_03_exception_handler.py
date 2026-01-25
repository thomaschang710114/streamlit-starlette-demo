import streamlit as st

st.title("3. Exception Handlers")
st.caption("Custom Error Responses")

st.markdown("""
Exception handlers allow you to define custom responses for specific HTTP errors, 
providing a consistent and branded error experience across your application.
""")

st.divider()

st.subheader("Live Demo")

# Row 1: Titles and descriptions
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 💥 Test 500 Error")
    st.markdown("Trigger a server error intentionally:")

with col2:
    st.markdown("#### 🔍 Test 404 Error")
    st.markdown("Try a non-existent static file:")

with col3:
    st.markdown("#### 🎯 SPA Catch-all")
    st.markdown("Streamlit catches unknown paths:")

# Row 2: Buttons and captions
col1, col2, col3 = st.columns(3)

with col1:
    st.link_button(
        "Visit /api/trigger-error",
        url="/api/trigger-error",
        use_container_width=True,
    )
    st.caption("Custom styled 500 page!")

with col2:
    st.link_button(
        "Visit /landing/missing.html",
        url="/landing/missing.html", 
        use_container_width=True,
    )
    st.caption("Custom 404 on static mount!")

with col3:
    st.link_button(
        "Visit /random-page",
        url="/random-page",
        use_container_width=True,
    )
    st.caption("Streamlit's internal 404 UI!")

st.divider()

st.info("""
**💡 Benefits of Custom Exception Handlers:**
- **Brand Consistency**: Error pages match your app's design
- **Better UX**: Users get helpful messages instead of generic errors  
- **Easy Navigation**: Direct links back to safe pages
- **Centralized Logic**: Handle all errors in one place
""")
