#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import plotly.express as px
import streamlit as st

# Streamlit App Title
st.title("Interactive Sales Tracker Dashboard")

# Load Google Sheet data (publicly accessible)
st.write("Loading data from Google Sheets...")
try:
    # Replace this link with your public Google Sheet link
    sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=2006560046"
    data = pd.read_csv(sheet_url)
    st.write("Data successfully loaded!")
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Ensure the Date column is in datetime format
try:
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Handles invalid dates
except Exception as e:
    st.error(f"Failed to parse 'Date' column: {e}")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")
ac_name = st.sidebar.selectbox("Select AC Name:", ["All"] + data['AC Name'].dropna().unique().tolist())
start_date = st.sidebar.date_input("Start Date", value=data['Date'].min())
end_date = st.sidebar.date_input("End Date", value=data['Date'].max())

# Filter Data
try:
    filtered_data = data.copy()
    if ac_name != "All":
        filtered_data = filtered_data[filtered_data['AC Name'] == ac_name]
    filtered_data = filtered_data[
        (filtered_data['Date'] >= pd.to_datetime(start_date)) &
        (filtered_data['Date'] <= pd.to_datetime(end_date))
    ]
except Exception as e:
    st.error(f"Failed to filter data: {e}")
    st.stop()

# Aggregated Metrics
try:
    summary = filtered_data.groupby('AC Name').agg({
        'Cash-in': 'sum',
        'Enrl': 'sum',
        'SGR Conversion': 'sum',
        'Fresh Leads': 'sum',
        'SGR Leads': 'sum',
        'Overall Leads': 'sum'
    }).reset_index()
except Exception as e:
    st.error(f"Failed to aggregate data: {e}")
    st.stop()

# Display Filtered Data
st.header("Filtered Data")
st.dataframe(filtered_data)

# Visualization
st.header("Performance Metrics by AC")
if not summary.empty:
    try:
        fig = px.bar(summary, x='AC Name', y=['Cash-in', 'Enrl', 'SGR Conversion'], barmode='group',
                     title="Performance Metrics by AC")
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Failed to generate visualization: {e}")
else:
    st.write("No data available for the selected filters.")
