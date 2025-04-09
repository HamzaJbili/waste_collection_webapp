# ui_components.py

import streamlit as st
from auth import save_users, get_users

def apply_styling():
    st.markdown("""
        <style>
            body {
                background-color: #f4f6f8;
                font-family: 'Segoe UI', sans-serif;
            }
            .title-style {
                font-size: 38px;
                font-weight: 900;
                padding-bottom: 20px;
                color: #003366;
            }
            .card {
                background: white;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.05);
                margin-bottom: 1.5rem;
            }
            .sidebar .sidebar-content {
                background-color: #ffffff;
                border-right: 1px solid #e6e6e6;
            }
            .stButton>button {
                background-color: #1a73e8;
                color: white;
                font-weight: 600;
                border: none;
                border-radius: 10px;
                padding: 0.5rem 1rem;
                transition: background-color 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #155ec2;
            }
            .stTextInput>div>div>input {
                border-radius: 8px;
            }
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def show_logo_title():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.image("https://i.imgur.com/fxyD8rF.png", width=100)
    st.markdown("<div class='title-style'>🚛 WasteTrack: Smart Waste Collection</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def show_sidebar(settings):
    st.sidebar.markdown("## 👤 Welcome")
    st.sidebar.info(f"👋 You are logged in as **{st.session_state.user}**")

    if st.session_state.user == "admin":
        st.sidebar.markdown("### ➕ Add Entries")

        new_vehicle = st.sidebar.text_input("🚗 Add Vehicle")
        if st.sidebar.button("Add Vehicle"):
            if new_vehicle:
                settings["vehicles"].append(new_vehicle)
                from data_handler import save_settings
                save_settings(settings)
                st.sidebar.success("✅ Vehicle added.")

        new_circuit = st.sidebar.text_input("🗺️ Add Circuit")
        if st.sidebar.button("Add Circuit"):
            if new_circuit:
                settings["circuits"].append(new_circuit)
                from data_handler import save_settings
                save_settings(settings)
                st.sidebar.success("✅ Circuit added.")

        new_employee = st.sidebar.text_input("👷 Add Employee")
        if st.sidebar.button("Add Employee"):
            if new_employee:
                settings["employees"].append(new_employee)
                from data_handler import save_settings
                save_settings(settings)
                st.sidebar.success("✅ Employee added.")

        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔐 User Management")

        users = get_users()
        new_user = st.sidebar.text_input("🆕 New Username")
        new_pass = st.sidebar.text_input("🔑 New Password", type="password")
        if st.sidebar.button("Create User"):
            if new_user and new_pass:
                if new_user in users:
                    st.sidebar.warning("⚠️ Username already exists.")
                else:
                    import hashlib
                    users[new_user] = hashlib.sha256(new_pass.encode()).hexdigest()
                    save_users(users)
                    st.sidebar.success("🎉 User created successfully.")
