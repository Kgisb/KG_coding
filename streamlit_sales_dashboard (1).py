import pandas as pd
import streamlit as st

# Load Google Sheet data
@st.cache_data
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=2006560046"
    data = pd.read_csv(sheet_url)
    data['Date'] = pd.to_datetime(data['Date'])  # Ensure Date column is datetime
    return data

data = load_data()

# App Title
st.title("Data Filter and Sort Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
ac_names = ["All"] + data['AC Name'].unique().tolist()
selected_ac_name = st.sidebar.selectbox("Select AC Name:", ac_names)

start_date = st.sidebar.date_input("Start Date", value=data['Date'].min().date())
end_date = st.sidebar.date_input("End Date", value=data['Date'].max().date())

# Filter and sort the data
def filter_and_sort_data(ac_name, start_date, end_date):
    filtered_data = data.copy()

    # Filter by AC Name if not "All"
    if ac_name != "All":
        filtered_data = filtered_data[filtered_data['AC Name'] == ac_name]

    # Filter by date range
    filtered_data = filtered_data[
        (filtered_data['Date'] >= pd.to_datetime(start_date)) &
        (filtered_data['Date'] <= pd.to_datetime(end_date))
    ]

    # Sort by Date
    filtered_data = filtered_data.sort_values(by="Date")
    return filtered_data

# Apply Filters
filtered_data = filter_and_sort_data(selected_ac_name, start_date, end_date)

# Display Filtered Data
st.subheader(f"Filtered Data ({len(filtered_data)} rows):")
st.dataframe(filtered_data)

# Download Filtered Data
csv = filtered_data.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv",
)
