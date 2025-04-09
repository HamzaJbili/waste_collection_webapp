# main.py - WasteTrack Entry Point

import streamlit as st
import pandas as pd
from datetime import datetime, time
from auth import login_user, init_session
from data_handler import load_data, save_data, load_settings
from ui_components import apply_styling, show_logo_title, show_sidebar
from dashboard import show_kpis_dashboard
from map_tools import show_map_tab
from config import DATA_FILE
import plotly.express as px

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

# --- Custom Navigation ---
nav = st.sidebar.radio("🔍 Navigate", [
    "📝 Add Entry", 
    "📈 Dashboard", 
    "📊 Raw Data", 
    "🗺️ Circuit Map", 
    "💳 Plans"
])

# --- Tab: Add Entry ---
if nav == "📝 Add Entry":
    st.markdown("<div class='title-style'>📝 Log Waste Collection</div>", unsafe_allow_html=True)
    with st.container():
        with st.form("add_entry", border=True):
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
            submitted = st.form_submit_button("➕ Submit Entry")

            if submitted:
                duration = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).total_seconds() / 60.0
                new_row = pd.DataFrame([[date, vehicle, circuit, trips, start_time.strftime("%H:%M"), end_time.strftime("%H:%M"),
                                         round(duration, 2), distance, fuel, load, receipt]], columns=data.columns)
                data = pd.concat([data, new_row], ignore_index=True)
                save_data(data)
                st.success("🎉 Entry added successfully!")

# --- Tab: Dashboard ---
elif nav == "📈 Dashboard":
    st.markdown("<div class='title-style'>📊 Dashboard Overview</div>", unsafe_allow_html=True)
    show_kpis_dashboard(data)

    # ➕ Bonus Chart: Waste Composition Breakdown
    st.markdown("### 🧪 Waste Fraction Characterization")
    fraction_data = {
        "Fraction": ["Organic", "Plastic", "Glass", "Metal", "Paper", "Other"],
        "Percentage": [45, 20, 10, 5, 15, 5]
    }
    df_fraction = pd.DataFrame(fraction_data)
    fig = px.pie(df_fraction, values='Percentage', names='Fraction', title="Composition of Waste Collected")
    st.plotly_chart(fig, use_container_width=True)

# --- Tab: Raw Data ---
elif nav == "📊 Raw Data":
    st.markdown("<div class='title-style'>📄 Collected Data</div>", unsafe_allow_html=True)
    st.dataframe(data, use_container_width=True)
    st.download_button("⬇️ Download CSV", data.to_csv(index=False), "waste_data.csv")

# --- Tab: Map ---
elif nav == "🗺️ Circuit Map":
    st.markdown("<div class='title-style'>🗺️ Circuit View</div>", unsafe_allow_html=True)
    show_map_tab(settings)

# --- Tab: Subscription ---
elif nav == "💳 Plans":
    st.markdown("<div class='title-style'>💳 Subscription Plans</div>", unsafe_allow_html=True)
    st.info("Test payment setup using Stripe. Switch to live keys in production.")
    st.markdown("""
    <div class='card'>
        <h4>🚀 Starter Plan — <span style='color:#2196F3;'>$29/month</span></h4>
        ✅ 3 users<br>
        ✅ 1 zone<br>
        ✅ Access to KPI Dashboard<br><br>
        <a href="https://buy.stripe.com/test_8wM6qX8wo1YUgYEaEE" target="_blank">
            <button style='background-color:#2196F3; color:white; border:none; padding:0.6rem 1.2rem; border-radius:8px;'>Pay with Stripe</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <hr style="margin-top: 3rem;">
    <center style='color:gray'>© 2025 WasteTrack • Smart Waste Management Platform</center>
""", unsafe_allow_html=True)
