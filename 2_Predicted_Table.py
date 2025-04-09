import streamlit as st
import pandas as pd

# Load data
df = pd.read_excel("D:/Motherson/PREDICTED_DATA_1.xlsx", parse_dates=["start_week_date"])
df['item_code'] = df['item_code'].astype(str)

st.title("📋 Predicted Demand Table")

# Initialize session state for filter reset
if "clear_filters" not in st.session_state:
    st.session_state.clear_filters = False

# Sidebar: Clear Filters button
if st.sidebar.button("🔄 Clear Filters"):
    st.session_state.clear_filters = True
else:
    st.session_state.clear_filters = False

# Sidebar: Date filter
min_date = df['start_week_date'].min()
selected_date = st.sidebar.date_input("Show data from date:", min_value=min_date, value=min_date)

# Apply filters
if st.session_state.clear_filters:
    filtered_df = df[df['predicted_demand'] > 0]
    st.info("Filters cleared. Showing all predicted demand data.")
else:
    # Filter 1: Plant
    plants = sorted(df['org'].unique())
    selected_plant = st.sidebar.selectbox("Select Plant", plants)

    filtered_df = df[df['org'] == selected_plant]

    # Filter 2: Item Code
    item_codes = sorted(filtered_df['item_code'].unique())
    selected_item = st.sidebar.selectbox("Select Item Code", item_codes)

    filtered_df = filtered_df[filtered_df['item_code'] == selected_item]

    # Filter 3: Description
    descriptions = sorted(filtered_df['description'].unique())
    selected_desc = st.sidebar.selectbox("Select Description", descriptions)

    filtered_df = filtered_df[filtered_df['description'] == selected_desc]
    filtered_df = filtered_df[filtered_df['predicted_demand'] > 0]

# Apply date filter
filtered_df = filtered_df[filtered_df['start_week_date'] >= pd.to_datetime(selected_date)]

# Display table
if not filtered_df.empty:
    st.dataframe(
        filtered_df[['start_week_date', 'item_code', 'description', 'predicted_demand']]
        .sort_values('start_week_date'),
        use_container_width=True
    )

    # Download filtered data
    csv = filtered_df[['start_week_date', 'item_code', 'description', 'predicted_demand']] \
        .sort_values('start_week_date') \
        .to_csv(index=False)

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="filtered_predicted_demand.csv",
        mime="text/csv"
    )
else:
    st.warning("No predicted demand data found for selected filters and date.")
