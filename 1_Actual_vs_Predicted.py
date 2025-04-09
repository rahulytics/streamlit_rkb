import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("D:/Motherson/PREDICTED_DATA_1.xlsx", parse_dates=["start_week_date"])
df['item_code'] = df['item_code'].astype(str)

st.title("📊 Actual vs Predicted Demand")

# Initialize session state for reset
if "clear_filters" not in st.session_state:
    st.session_state.clear_filters = False

# Clear Filters button
if st.sidebar.button("🔄 Clear Filters"):
    st.session_state.clear_filters = True
else:
    st.session_state.clear_filters = False

# Apply filters
if st.session_state.clear_filters:
    chart_df = df.copy()
    st.info("Filters cleared. Showing complete data.")
    y_col = "predicted_demand"  # default to predicted
else:
    # Sidebar - Step-by-step dependent filters
    plants = sorted(df['org'].unique())
    selected_plant = st.sidebar.selectbox("Select Plant", plants)

    filtered_df = df[df['org'] == selected_plant]

    item_codes = sorted(filtered_df['item_code'].unique())
    selected_item = st.sidebar.selectbox("Select Item Code", item_codes)

    filtered_df = filtered_df[filtered_df['item_code'] == selected_item]

    descriptions = sorted(filtered_df['description'].unique())
    selected_desc = st.sidebar.selectbox("Select Description", descriptions)

    filtered_df = filtered_df[filtered_df['description'] == selected_desc]

    data_type = st.sidebar.selectbox("Select Data Type", ["Actual (Past 1 Year)", "Predicted"])

    # Final filter
    if data_type == "Actual (Past 1 Year)":
        chart_df = filtered_df[filtered_df['actual_demand'] > 0]
        chart_df = chart_df[chart_df['start_week_date'] >= (chart_df['start_week_date'].max() - pd.DateOffset(days=365))]
        y_col = "actual_demand"
    else:
        chart_df = filtered_df[filtered_df['predicted_demand'] > 0]
        y_col = "predicted_demand"

# Plot
if not chart_df.empty:
    fig = px.line(chart_df, x='start_week_date', y=y_col,
                  title=f"{y_col.replace('_', ' ').title()} for Item {selected_item if not st.session_state.clear_filters else ''}",
                  markers=True)
    fig.update_layout(xaxis_title="Week Start Date", yaxis_title="Demand", height=500)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")
