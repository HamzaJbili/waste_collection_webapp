# ui_components.py

import streamlit as st

def apply_styling():
    dark_mode = st.session_state.get("dark_mode", False)

    if dark_mode:
        background = "#1e1e1e"
        text_color = "#fafafa"
        card_bg = "#2c2c2c"
    else:
        background = "#f9f9f9"
        text_color = "#222"
        card_bg = "#ffffff"

    st.markdown(f"""
        <style>
            body {{
                background-color: {background};
                color: {text_color};
                font-family: 'Segoe UI', sans-serif;
            }}
            .logo-title {{
                background: linear-gradient(90deg, #a2facf 0%, #64acff 100%);
                padding: 1.5rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                color: #fff;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            }}
            section[data-testid="stSidebar"] {{
                background-color: {card_bg};
            }}
            .stTextInput, .stNumberInput, .stSelectbox {{
                font-size: 16px !important;
                border-radius: 10px;
            }}
            button {{
                border-radius: 8px !important;
            }}
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
