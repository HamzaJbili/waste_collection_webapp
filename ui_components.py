# ui_components.py

import streamlit as st

def apply_styling():
   def apply_styling():
def apply_styling():
    st.markdown("""
        <style>
            html, body, [class*="css"]  {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(120deg, #f9f9f9, #e0f7fa);
                color: #333;
            }
            .title-style {
                font-size: 36px;
                font-weight: 800;
                padding-bottom: 10px;
                color: #1b4965;
            }
            .card {
                background: white;
                border-radius: 16px;
                padding: 1rem;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s ease;
            }
            .card:hover {
                transform: scale(1.01);
            }
            .stButton>button {
                background-color: #1b4965;
                color: white;
                padding: 0.6rem 1.2rem;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #62b6cb;
                color: #fff;
            }
            .stSelectbox>div>div {
                font-size: 16px;
            }
            .stTextInput>div>div>input {
                font-size: 16px;
                border-radius: 8px;
            }
            .stTabs [role="tab"] {
                background-color: #fff;
                padding: 0.8rem 1.2rem;
                margin-right: 10px;
                border-radius: 12px 12px 0 0;
                font-weight: 600;
                color: #1b4965;
                border: 1px solid #ddd;
            }
            .stTabs [aria-selected="true"] {
                background: #1b4965;
                color: white;
                border-bottom: 2px solid white;
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
