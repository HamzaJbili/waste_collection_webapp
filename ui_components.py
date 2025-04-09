# ui_components.py

import streamlit as st

def apply_styling():
   def apply_styling():
    st.markdown("""
        <style>
            body {
                background: linear-gradient(135deg, #F5F7FA 0%, #c3cfe2 100%) !important;
            }

            .title-style {
                font-size: 38px; 
                font-weight: 800; 
                padding-bottom: 15px;
            }

            .card {
                background: rgba(255, 255, 255, 0.8); 
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                backdrop-filter: blur(8px);
                margin-bottom: 2rem;
            }

            .stTextInput>div>div>input, 
            .stButton>button, 
            .stSelectbox>div>div>div {
                font-size: 16px !important;
                border-radius: 10px;
                padding: 0.4rem 0.75rem;
            }

            .stButton>button:hover {
                background-color: #4CAF50 !important;
                color: white !important;
                box-shadow: 0 0 0.5rem rgba(76, 175, 80, 0.5);
                transition: 0.3s ease-in-out;
            }

            .stDownloadButton>button {
                background-color: #2196F3 !important;
                color: white !important;
                border-radius: 8px;
                padding: 0.5rem 1rem;
            }

            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)


def show_logo_title():
    st.markdown("""
        <div class='logo-title'>
            <h1>🚛 WasteTrack</h1>
            <p>Smart Waste Collection & Environmental Analytics</p>
        </div>
    """, unsafe_allow_html=True)


def show_sidebar(settings):
    st.sidebar.markdown("## 🔧 Settings Panel")

    # Toggle Theme
    dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.get("dark_mode", False))
    st.session_state.dark_mode = dark_mode

    # Show user info
    if "user" in st.session_state:
        user = st.session_state.user
        st.sidebar.success(f"👋 Logged in as `{user}`")
    else:
        user = "guest"
        st.sidebar.warning("Not logged in")

    # Admin panel only visible to admin
    if user == "admin":
        st.sidebar.markdown("---")
        st.sidebar.subheader("⚙️ Admin Settings")

        new_vehicle = st.text_input("Add Vehicle")
        if st.button("Add Vehicle"):
            if new_vehicle:
                settings["vehicles"].append(new_vehicle)
                from data_handler import save_settings
                save_settings(settings)
                st.success(f"🚛 Added vehicle: {new_vehicle}")

        new_circuit = st.text_input("Add Circuit")
        if st.button("Add Circuit"):
            if new_circuit:
                settings["circuits"].append(new_circuit)
                from data_handler import save_settings
                save_settings(settings)
                st.success(f"🗺️ Added circuit: {new_circuit}")

        new_employee = st.text_input("Add Employee")
        if st.button("Add Employee"):
            if new_employee:
                settings["employees"].append(new_employee)
                from data_handler import save_settings
                save_settings(settings)
                st.success(f"👷 Added employee: {new_employee}")

    st.sidebar.markdown("---")
    st.sidebar.caption("© 2025 WasteTrack")
