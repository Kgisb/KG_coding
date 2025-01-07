#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
import sys

# Function to install a package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure required packages are installed
try:
    import pandas as pd
    import plotly.express as px
    import streamlit as st
except ImportError as e:
    package = e.name
    print(f"Installing missing package: {package}")
    install(package)
    import pandas as pd
    import plotly.express as px
    import streamlit as st

# Streamlit App Title
st.title("Interactive Sales Tracker Dashboard")

# Load Google Sheet data (publicly accessible)
st.write("Loading data from Google Sheets...")
try:
    sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=2006560046"
    data = pd.read_csv(sheet_url)
    st.write("Data successfully loaded!")
except Exception as e:
    st.error("Failed to load data. Please check the Google Sheet link and ensure it is publicly accessible.")
    st.stop()

# Ensure the Date column is in datetime format
try:
    data['Date'] = pd.to_datetime(data['Date'])
except Exception as e:
    st.error("Failed to convert 'Date' column to datetime format. Please check the data.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")
ac_name = st.sidebar.selectbox("Select AC Name:", ["All"] + data['AC Name'].unique().tolist())
start_date = st.sidebar.date_input("Start Date", value=data['Date'].min())
end_date = st.sidebar.date_input("End Date", value=data['Date'].max())

# Filter Data
filtered_data = data.copy()
if ac_name != "All":
    filtered_data = filtered_data[filtered_data['AC Name'] == ac_name]

try:
    filtered_data = filtered_data[
        (filtered_data['Date'] >= pd.to_datetime(start_date)) &
        (filtered_data['Date'] <= pd.to_datetime(end_date))
    ]
except Exception as e:
    st.error("Failed to filter data by date range. Please check the input dates.")
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
    st.error("Failed to aggregate data. Please check the data structure.")
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
        st.error("Failed to generate visualization. Please check the data.")
else:
    st.write("No data available for the selected filters.")
