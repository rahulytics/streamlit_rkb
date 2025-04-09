import streamlit as st
import pandas as pd

# Load data
df = pd.read_excel("PREDICTED_DATA_1.xlsx", parse_dates=["start_week_date"])
df['item_code'] = df['item_code'].astype(str)

# Page config
st.set_page_config(page_title="Predicted Demand Table", layout="wide")
st.title("📋 Predicted Demand Table")

# Custom styling
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
    }
    label {
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.markdown("### 🧭 Navigation")

    # Date
    min_date = df['start_week_date'].min()
    selected_date = st.date_input("📅 Show data from:", min_value=min_date, value=min_date)

    # Filter: Plant
    plant_options = sorted(df['org'].unique())
    selected_plant = st.selectbox("🏭 Select Plant", plant_options)

    # Filter: Item
    item_options = sorted(df[df['org'] == selected_plant]['item_code'].unique()) if selected_plant else []
    selected_item = st.selectbox("📦 Select Item Code", item_options)

    # Filter: Description
    desc_options = sorted(df[(df['org'] == selected_plant) & (df['item_code'] == selected_item)]['description'].unique()) if selected_item else []
    selected_desc = st.selectbox("📝 Select Description", desc_options)

# Filter data based on selections
filtered_df = df[
    (df['org'] == selected_plant) &
    (df['item_code'] == selected_item) &
    (df['description'] == selected_desc) &
    (df['predicted_demand'] >= 0) &
    (df['start_week_date'] >= pd.to_datetime(selected_date))
]

# Display table
if not filtered_df.empty:
    display_df = filtered_df[['start_week_date', 'item_code', 'description', 'predicted_demand']] \
        .sort_values('start_week_date') \
        .rename(columns={
            'start_week_date': 'Start Week Date',
            'item_code': 'Item Code',
            'description': 'Description',
            'predicted_demand': 'Predicted Demand'
        })

    st.dataframe(display_df, use_container_width=True)

    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="filtered_predicted_demand.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ No predicted demand data found for the selected filters and date.")
