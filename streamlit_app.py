import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard Demo", layout="wide")

st.title("📊 Executive Dashboard")

# Sidebar Configuration
st.sidebar.header("Configuration")
st.sidebar.markdown("Use the slider below to filter the data based on revenue threshold.")
filter_value = st.sidebar.slider("Minimum Revenue Threshold", min_value=0, max_value=100, value=25)

# Placeholder Data Generation
np.random.seed(42) # For reproducible results
dates = pd.date_range(start="2024-01-01", periods=100)
data = pd.DataFrame({
    "Date": dates,
    "Revenue": np.random.randint(10, 100, size=100),
    "Users": np.random.randint(100, 500, size=100),
    "Category": np.random.choice(["Electronics", "Fashion", "Home", "Sports"], size=100)
})

# Filter Logic
filtered_data = data[data["Revenue"] >= filter_value]

# Metrics Section
st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)

total_revenue = filtered_data['Revenue'].sum()
avg_users = int(filtered_data['Users'].mean()) if not filtered_data.empty else 0
# Simulating a growth metric calculation
previous_revenue = total_revenue * 0.9 
delta_val = total_revenue - previous_revenue

with col1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,}", delta=f"{((total_revenue - previous_revenue)/previous_revenue)*100:.1f}%" if previous_revenue else "0%")
with col2:
    st.metric(label="Avg Active Users", value=f"{avg_users}")
with col3:
    st.metric(label="Transaction Count", value=f"{len(filtered_data)}")

st.divider()

# Charts Section
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Revenue Trend")
    if not filtered_data.empty:
        st.line_chart(filtered_data.set_index("Date")["Revenue"])
    else:
        st.info("No data to display with current filter.")

with col_chart2:
    st.subheader("Users by Category")
    if not filtered_data.empty:
        category_data = filtered_data.groupby("Category")["Users"].sum()
        st.bar_chart(category_data)
    else:
        st.info("No data to display with current filter.")

# Data Table Section
st.subheader("Detailed Data View")
st.text(f"Showing top 10 records matching criteria (Total: {len(filtered_data)})")
st.dataframe(filtered_data.head(10), use_container_width=True)