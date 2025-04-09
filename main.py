# main.py - WasteTrack Entry Point
import streamlit as st
from auth import login_user, init_session
from data_handler import load_data, save_data, load_settings
from ui_components import apply_styling, show_logo_title, show_sidebar
from dashboard import show_kpis_dashboard
from map_tools import show_map_tab
from config import DATA_FILE
import pandas as pd

# --- Init ---
st.set_page_config(page_title="WasteTrack | Smart Waste Management", layout="wide")
apply_styling()
init_session()

# --- Auth ---
if not st.session_state.logged_in:
    login_user()
    st.stop()

# --- Data ---
data = load_data()
settings = load_settings()

# --- UI ---
show_logo_title()
show_sidebar(settings)

# --- Tabs ---
tabs = st.tabs(["📋 Add Entry", "📈 KPIs Dashboard", "📊 Raw Data", "🗘️ Circuit Map", "💳 Subscription"])

# --- Tab 0: Add Entry ---
with tabs[0]:
    st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
    """, unsafe_allow_html=True)

    st.markdown("### 📋 Add New Collection Entry")
    from datetime import datetime, time

    with st.form("add_entry"):
        date = st.date_input("Date")
        vehicle = st.selectbox("Vehicle", options=settings.get("vehicles", []))
        circuit = st.selectbox("Circuit", options=settings.get("circuits", []))
        trips = st.number_input("Number of Trips", min_value=0)
        start_time = st.time_input("Start Time", value=time(7, 0))
        end_time = st.time_input("End Time", value=time(15, 0))
        distance = st.number_input("Distance (km)", min_value=0.0)
        fuel = st.number_input("Fuel Consumption (L)", min_value=0.0)
        load = st.number_input("Load (Tons)", min_value=0.0)
        receipt = st.text_input("Receipt Number")
        submitted = st.form_submit_button("Add Entry")

        if submitted:
            duration = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).total_seconds() / 60.0
            new_row = pd.DataFrame([[
                date, vehicle, circuit, trips, start_time.strftime("%H:%M"), end_time.strftime("%H:%M"),
                round(duration, 2), distance, fuel, load, receipt
            ]], columns=data.columns)
            data = pd.concat([data, new_row], ignore_index=True)
            save_data(data)
            st.success("Entry added successfully")

    st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 1: Dashboard ---
with tabs[1]:
    show_kpis_dashboard(data)

# --- Tab 2: Raw Data ---
with tabs[2]:
    st.markdown("### 📊 Raw Data")
    st.dataframe(data, use_container_width=True)
    st.download_button("⬇️ Download CSV", data.to_csv(index=False), "waste_data.csv")

# --- Tab 3: Map ---
with tabs[3]:
    show_map_tab(settings)

# --- Tab 4: Subscription ---
with tabs[4]:
    st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); margin-top: 2rem;">
            <h3 style="color:#1e5631;">💳 Subscribe to Access</h3>
            <p>Below is a <strong>test</strong> payment setup using Stripe.<br>In production, you can switch to live keys.</p>
            <h4>Starter Plan: <span style="color:#4caf50;">$29/month</span></h4>
            <ul style="line-height:1.8;">
                <li>✅ 3 Users</li>
                <li>✅ 1 Zone</li>
                <li>✅ KPI Dashboard Access</li>
            </ul>
            <a href="https://buy.stripe.com/test_8wM6qX8wo1YUgYEaEE" target="_blank" style="
                display:inline-block; padding: 0.75rem 1.5rem; background:#4caf50; color:white; text-decoration:none; 
                border-radius:8px; font-weight:bold; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                Pay with Stripe (Test Mode)
            </a>
        </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <hr style="margin-top: 3rem;">
    <p style='text-align: center; color: gray; font-size: 0.9rem'>
        © 2025 <strong>WasteTrack</strong> • Smart Waste Management Platform
    </p>
""", unsafe_allow_html=True)
