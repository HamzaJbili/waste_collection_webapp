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
    st.markdown("### 💳 Subscribe to Access")
    st.info("Below is a test payment setup using Stripe. In production, you can switch to live keys.")
    st.markdown("**Starter Plan: $29/month**")
    st.markdown("✅ 3 users\n✅ 1 zone\n✅ KPI dashboard")
    st.link_button("Pay with Stripe (Test Mode)", "https://buy.stripe.com/test_8wM6qX8wo1YUgYEaEE")

# --- Footer ---
st.markdown("""
    <hr>
    <center style='color:gray'>© 2025 WasteTrack • Smart Waste Management Platform</center>
""", unsafe_allow_html=True)
