# ui_components.py

import streamlit as st
from auth import save_users, get_users  # ✅ Add get_users here

def apply_styling():
    st.markdown("""
        <style>
            html, body, [class*="css"] {
                font-family: 'Segoe UI', sans-serif;
            }

            .title-style {
                font-size: 36px;
                font-weight: 800;
                padding-bottom: 10px;
                color: #2E8B57;
            }

            .metric-style {
                font-size: 24px;
                font-weight: bold;
            }

            .card {
                background: #ffffff;
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
                margin-bottom: 1rem;
            }

            .stTextInput>div>div>input, 
            .stButton>button, 
            .stSelectbox>div>div>div {
                font-size: 16px !important; 
                border-radius: 12px !important;
            }

            .stButton>button {
                background-color: #2E8B57 !important;
                color: white !important;
            }

            .stButton>button:hover {
                background-color: #256d45 !important;
            }

            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)


def show_logo_title():
    st.image("https://cdn-icons-png.flaticon.com/512/2984/2984615.png", width=60)
    st.markdown("<div class='title-style'>🚛 WasteTrack: Smart Waste Collection</div>", unsafe_allow_html=True)

def show_sidebar(settings):
    st.sidebar.markdown("## 👤 User Panel")
    st.sidebar.info(f"👋 Logged in as: `{st.session_state.user}`")

    if st.session_state.user == "admin":
        with st.sidebar.expander("⚙️ Admin Settings", expanded=True):
            st.subheader("Manage Settings")

            new_vehicle = st.text_input("Add Vehicle")
            if st.button("Add Vehicle") and new_vehicle:
                settings["vehicles"].append(new_vehicle)
                from data_handler import save_settings
                save_settings(settings)
                st.success("Vehicle added.")

            new_circuit = st.text_input("Add Collection Circuit")
            if st.button("Add Circuit") and new_circuit:
                settings["circuits"].append(new_circuit)
                from data_handler import save_settings
                save_settings(settings)
                st.success("Circuit added.")

            new_employee = st.text_input("Add Employee")
            if st.button("Add Employee") and new_employee:
                settings["employees"].append(new_employee)
                from data_handler import save_settings
                save_settings(settings)
                st.success("Employee added.")

        with st.sidebar.expander("🔑 User Management", expanded=False):
            users = get_users()  # ✅ Fixed: Now this is valid!
            st.subheader("Create New Account")
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type="password")

            if st.button("Create User") and new_user and new_pass:
                if new_user in users:
                    st.warning("Username already exists.")
                else:
                    import hashlib
                    users[new_user] = hashlib.sha256(new_pass.encode()).hexdigest()
                    save_users(users)
                    st.success("User created successfully.")
