import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nassau Supply Chain Dashboard", layout="wide")

st.title("📦 Nassau Candy Distributor - Supply Chain Analytics")

df = pd.read_csv("cleaned_data.csv")

# Sidebar Filters
st.sidebar.header("Filters")

region = st.sidebar.selectbox("Select Region", ["All"] + list(df['Region'].unique()))
ship_mode = st.sidebar.selectbox("Select Ship Mode", ["All"] + list(df['Ship Mode'].unique()))

filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == region]

if ship_mode != "All":
    filtered_df = filtered_df[filtered_df['Ship Mode'] == ship_mode]

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Shipments", filtered_df.shape[0])
col2.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col3.metric("Avg Lead Time", round(filtered_df['Shipping Lead Time'].mean(),2))

delay_rate = (filtered_df['Shipping Lead Time'] > filtered_df['Shipping Lead Time'].mean()).mean() * 100
col4.metric("Delay Rate (%)", round(delay_rate,2))
# Route Chart
route_summary = filtered_df.groupby('State/Province').agg(
    Shipments=('Order ID', 'count')
).reset_index().sort_values('Shipments', ascending=False)

fig = px.bar(route_summary.head(10),
             x='State/Province',
             y='Shipments',
             title="Top 10 States by Shipment Volume")

st.plotly_chart(fig, use_container_width=True)

# Ship Mode Chart
ship_mode_summary = filtered_df.groupby('Ship Mode').agg(
    Avg_Lead_Time=('Shipping Lead Time', 'mean')
).reset_index()

fig2 = px.bar(ship_mode_summary,
              x='Ship Mode',
              y='Avg_Lead_Time',
              title="Average Lead Time by Ship Mode")

st.plotly_chart(fig2, use_container_width=True)
# -----------------------------
# Sales by Region Chart
# -----------------------------

region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()

fig3 = px.pie(region_sales,
              values='Sales',
              names='Region',
              title="Sales Distribution by Region")

st.plotly_chart(fig3, use_container_width=True)
# -----------------------------
# Route Efficiency Leaderboard
# -----------------------------

# Route Efficiency Leaderboard
route_summary = filtered_df.groupby('State/Province').agg(
    Avg_Lead_Time=('Shipping Lead Time', 'mean'),
    Shipments=('Order ID', 'count'),
    Total_Sales=('Sales', 'sum')
).reset_index()

route_summary = route_summary.sort_values('Avg_Lead_Time').reset_index(drop=True)

st.subheader("Route Efficiency Leaderboard (Fastest States)")
st.dataframe(route_summary.head(15), hide_index=True)
