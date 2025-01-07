
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import plotly.express as px
import streamlit as st

# Streamlit App Title
st.title("Interactive Sales Tracker Dashboard")

# Load Google Sheet data (publicly accessible)
sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=2006560046"
data = pd.read_csv(sheet_url)

# Ensure the Date column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Sidebar Filters
st.sidebar.header("Filters")
ac_name = st.sidebar.selectbox("Select AC Name:", ["All"] + data['AC Name'].unique().tolist())
start_date = st.sidebar.date_input("Start Date", value=data['Date'].min())
end_date = st.sidebar.date_input("End Date", value=data['Date'].max())

# Filter Data
filtered_data = data.copy()
if ac_name != "All":
    filtered_data = filtered_data[filtered_data['AC Name'] == ac_name]

filtered_data = filtered_data[
    (filtered_data['Date'] >= pd.to_datetime(start_date)) &
    (filtered_data['Date'] <= pd.to_datetime(end_date))
]

# Aggregated Metrics
summary = filtered_data.groupby('AC Name').agg({
    'Cash-in': 'sum',
    'Enrl': 'sum',
    'SGR Conversion': 'sum',
    'Fresh Leads': 'sum',
    'SGR Leads': 'sum',
    'Overall Leads': 'sum'
}).reset_index()

# Display Filtered Data
st.header("Filtered Data")
st.dataframe(filtered_data)

# Visualization
st.header("Performance Metrics by AC")
if not summary.empty:
    fig = px.bar(summary, x='AC Name', y=['Cash-in', 'Enrl', 'SGR Conversion'], barmode='group',
                 title="Performance Metrics by AC")
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected filters.")
