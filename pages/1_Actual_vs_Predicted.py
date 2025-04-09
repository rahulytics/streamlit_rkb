import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("PREDICTED_DATA_1.xlsx", parse_dates=["start_week_date"])
df['item_code'] = df['item_code'].astype(str)

# Page setup
st.set_page_config(page_title="Actual vs Predicted Demand", layout="wide")
st.title("📊 Actual vs Predicted Demand Analysis")

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
    st.markdown("Use the filters below to explore demand trends.")

    selected_plant = st.selectbox("🏭 Select Plant", sorted(df['org'].unique()), key="plant")

    item_options = sorted(df[df['org'] == selected_plant]['item_code'].unique()) if selected_plant else []
    selected_item = st.selectbox("📦 Select Item Code", item_options, key="item")

    desc_options = sorted(df[(df['org'] == selected_plant) & (df['item_code'] == selected_item)]['description'].unique()) if selected_item else []
    selected_desc = st.selectbox("📝 Select Description", desc_options, key="desc")

    data_type = st.radio("📈 Select Data Type", ["Actual (Past 1 Year)", "Predicted"], key="type")

# Check all filters selected
if selected_plant and selected_item and selected_desc:
    filtered_df = df[
        (df['org'] == selected_plant) &
        (df['item_code'] == selected_item) &
        (df['description'] == selected_desc)
    ]

    chart_df = pd.DataFrame()
    y_col = ""
    subtitle = f"Item {selected_item}"

    if data_type == "Actual (Past 1 Year)":
        chart_df = filtered_df[filtered_df['actual_demand'] > 0]
        chart_df = chart_df[chart_df['start_week_date'] >= (chart_df['start_week_date'].max() - pd.DateOffset(days=365))]
        y_col = "actual_demand"
    else:
        chart_df = filtered_df[filtered_df['predicted_demand'].notna()]
        chart_df = chart_df[chart_df['predicted_demand'] >= 0]
        y_col = "predicted_demand"

    if not chart_df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 Date Range", f"{chart_df['start_week_date'].min().date()} → {chart_df['start_week_date'].max().date()}")
        with col2:
            st.metric("📈 Avg Demand", f"{chart_df[y_col].mean():,.0f}")
        with col3:
            st.metric("🔝 Peak Demand", f"{chart_df[y_col].max():,.0f}")

        fig = px.line(
            chart_df.sort_values("start_week_date"),
            x='start_week_date',
            y=y_col,
            title=f"📊 {y_col.replace('_', ' ').title()} Trend - {subtitle}",
            markers=True,
            line_shape="linear",
            color_discrete_sequence=["#00C2FF"]
        )

        fig.update_traces(marker=dict(size=10))
        fig.update_layout(
            xaxis_title="Week Start Date",
            yaxis_title="Demand",
            height=500,
            template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
            font=dict(size=14),
            yaxis=dict(rangemode='tozero'),
            xaxis=dict(tickangle=-45, type='category')
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No data found for the selected filters.")
else:
    st.info("👈 Please select all filters to view the demand chart.")
