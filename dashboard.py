# dashboard.py

import streamlit as st
import pandas as pd

def show_kpis_dashboard(data: pd.DataFrame):
    st.markdown("### 📈 KPIs Overview")
    if not data.empty:
        today = pd.to_datetime("today").normalize()
        total_waste = data['Load_Tons'].sum()
        total_fuel = data['Fuel_Consumption'].sum()
        today_collected = data[data['Date'] == str(today.date())]['Load_Tons'].sum()
        avg_daily = data.groupby('Date')['Load_Tons'].sum().mean()
        projected_7d = round(avg_daily * 7, 2)
        projected_30d = round(avg_daily * 30, 2)
        cost_per_ton = total_fuel * 1.5 / total_waste if total_waste > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📊 Total Collected (Tons)", f"{total_waste:.2f}")
        col2.metric("🌍 Today Collected", f"{today_collected:.2f}")
        col3.metric("🔢 Cost/Ton Estimate", f"${cost_per_ton:.2f}")
        col4.metric("📈 7D Projection", f"{projected_7d} tons")

        st.line_chart(data.groupby('Date')['Load_Tons'].sum().rolling(window=3).mean(), height=250)
    else:
        st.info("No data available yet. Please add entries.")
