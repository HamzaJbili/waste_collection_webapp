# app.py
# Waste Collection Dashboard with Online Access and Admin Settings
# Streamlit app with user authentication, persistent settings, and KPIs tracking
# To run: streamlit run app.py


import streamlit as st
import pandas as pd
import hashlib
import json
import os
from datetime import datetime, time
from streamlit_folium import st_folium
import folium
from folium.plugins import Draw
import stripe

# --- Stripe Configuration ---
stripe.api_key = "sk_test_XXXXXXXXXXXXXXXXXXXXXXXX"  # Replace with your Stripe test secret key

# --- Authentication Setup ---
CREDENTIALS_FILE = "users.json"
SETTINGS_FILE = "settings.json"
DATA_FILE = "waste_data.csv"

# --- Load or Initialize Credentials ---
def load_users():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {
        "admin": hashlib.sha256("admin123".encode()).hexdigest()
    }

def save_users(users):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(users, file)

users = load_users()

# --- Authenticate Function ---
def login(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return users.get(username) == hashed_password

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if not st.session_state.logged_in:
    st.set_page_config(page_title="WasteTrack | Smart Waste Management", layout="wide")
    st.markdown("""
        <style>
            .main { background-color: #f0f2f6; }
            .block-container { padding-top: 2rem; padding-bottom: 2rem; }
            .stTextInput>div>div>input, .stButton>button, .stSelectbox>div>div>div { font-size: 16px !important; }
        </style>
    """, unsafe_allow_html=True)

    st.image("https://i.imgur.com/fxyD8rF.png", width=140)  # Placeholder for Earth–Mars logo
    st.markdown("## 🌍 WasteTrack: Intelligent Waste Collection")
    st.markdown("Please log in to access your dashboard.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("🔐 Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful. Please reload if not redirected.")
            st.stop()
        else:
            st.error("Invalid credentials")
    st.stop()

# --- Admin Settings ---
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"vehicles": [], "circuits": [], "employees": [], "zones": {}}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

settings = load_settings()

# --- Load or Initialize Data ---
if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE)
else:
    data = pd.DataFrame(columns=[
        'Date', 'Vehicle', 'Circuit', 'Trips', 'Start_Time', 'End_Time', 'Duration_Minutes',
        'Distance', 'Fuel_Consumption', 'Load_Tons', 'Receipt_No'
    ])

st.set_page_config(page_title="WasteTrack Dashboard", layout="wide")

st.markdown("""
    <style>
        .title-style { font-size:36px; font-weight:800; padding-bottom: 10px; }
        .metric-style { font-size:24px; font-weight:bold; }
    </style>
""", unsafe_allow_html=True)

st.image("https://i.imgur.com/fxyD8rF.png", width=100)
st.markdown("<div class='title-style'>🚛 WasteTrack: Smart Waste Collection</div>", unsafe_allow_html=True)
st.sidebar.markdown("## 👤 User Panel")
st.sidebar.success(f"Logged in as: {st.session_state.user}")

if st.session_state.user == "admin":
    with st.sidebar.expander("⚙️ Admin Settings", expanded=True):
        st.subheader("Manage Settings")
        new_vehicle = st.text_input("Add Vehicle")
        if st.button("Add Vehicle") and new_vehicle:
            settings["vehicles"].append(new_vehicle)
            save_settings(settings)
            st.success("Vehicle added.")

        new_circuit = st.text_input("Add Collection Circuit")
        if st.button("Add Circuit") and new_circuit:
            settings["circuits"].append(new_circuit)
            save_settings(settings)
            st.success("Circuit added.")

        new_employee = st.text_input("Add Employee")
        if st.button("Add Employee") and new_employee:
            settings["employees"].append(new_employee)
            save_settings(settings)
            st.success("Employee added.")

# --- Tabs Layout ---
tabs = st.tabs(["📋 Add Entry", "📈 KPIs Dashboard", "📊 Raw Data", "🗺️ Circuit Map", "💳 Subscription"])

with tabs[0]:
    st.markdown("### 📋 Add New Collection Entry")
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
            data.to_csv(DATA_FILE, index=False)
            st.success("Entry added successfully")

with tabs[1]:
    st.markdown("### 📈 KPIs Overview")
    if not data.empty:
        total_waste = data['Load_Tons'].sum()
        total_fuel = data['Fuel_Consumption'].sum()
        cost_per_ton = total_fuel * 1.5 / total_waste if total_waste > 0 else 0
        trips_per_circuit = data.groupby('Circuit')['Trips'].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Waste Collected (Tons)", f"{total_waste:.2f}")
        col2.metric("Total Fuel Used (L)", f"{total_fuel:.2f}")
        col3.metric("Estimated Cost per Ton ($)", f"{cost_per_ton:.2f}")

        st.subheader("Trips per Circuit")
        st.bar_chart(trips_per_circuit)
    else:
        st.info("No data available yet. Please add entries.")

with tabs[2]:
    st.markdown("### 📊 Raw Data")
    st.dataframe(data, use_container_width=True)
    st.download_button("⬇️ Download CSV", data.to_csv(index=False), "waste_data.csv")

with tabs[3]:
    st.markdown("### 🗺️ Collection Circuit Map")
    st.write("Draw or view collection zones. Circuits are stored in your settings.")

    # Initialize map
    m = folium.Map(location=[36.8, 10.1], zoom_start=11)
    draw = Draw(export=True)
    draw.add_to(m)

    # Display existing zones
    for name, geojson in settings.get("zones", {}).items():
        gj = folium.GeoJson(geojson, name=name)
        gj.add_to(m)

    # Display the map
    map_data = st_folium(m, width=700, height=500)

    if st.button("💾 Save Map Zones"):
        if map_data and 'all_drawings' in map_data:
            new_zones = {f"Zone_{i+1}": shape for i, shape in enumerate(map_data['all_drawings'])}
            settings["zones"] = new_zones
            save_settings(settings)
            st.success("Zones saved successfully.")

with tabs[4]:
    st.markdown("### 💳 Subscribe to Access")
    st.info("Below is a test payment setup using Stripe. In production, you can switch to live keys.")
    st.markdown("**Starter Plan: $29/month**")
    st.markdown("✅ 3 users\n✅ 1 zone\n✅ KPI dashboard")
    st.link_button("Pay with Stripe (Test Mode)", "https://buy.stripe.com/test_8wM6qX8wo1YUgYEaEE")  # replace with your real link
