# ui_components.py

import streamlit as st

def apply_styling():
    st.markdown("""
        <style>
            /* General tweaks */
            body {
                background: #f9f9f9;
                font-family: 'Segoe UI', sans-serif;
            }

            /* Logo & Title container */
            .logo-title {
                background: linear-gradient(90deg, #e9f5ec 0%, #ffffff 100%);
                padding: 2rem;
                margin-bottom: 1rem;
                border-radius: 15px;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.08);
            }

            /* Sidebar custom */
            section[data-testid="stSidebar"] {
                background-color: #f0f4f7;
                padding: 1rem;
                border-right: 1px solid #ccc;
            }

            /* Tabs styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 1rem;
            }

            /* Buttons */
            button[kind="primary"] {
                background-color: #4CAF50 !important;
                border: none;
                font-weight: bold;
            }

            /* Inputs */
            .stTextInput, .stNumberInput, .stSelectbox, .stDateInput, .stTimeInput {
                padding: 0.4rem;
                border-radius: 8px;
                border: 1px solid #ccc;
                background-color: #ffffff;
            }
        </style>
    """, unsafe_allow_html=True)

def show_logo_title():
    with st.container():
        st.markdown("""
            <div class="logo-title">
                <h1 style="display:flex; align-items:center;">
                    <span style="font-size:2rem; margin-right:10px;">🚛</span>
                    <span style="color: #2e7d32;">WasteTrack: Smart Waste Collection</span>
                </h1>
                <p>Your streamlined, eco-friendly waste management SaaS solution.</p>
            </div>
        """, unsafe_allow_html=True)

def show_sidebar(settings):
    st.sidebar.header("👤 User Panel")

    # ✅ Avoid AttributeError by checking if the key exists
    if "username" in st.session_state:
        st.sidebar.info(f"👋 Logged in as: `{st.session_state.username}`")

    with st.sidebar.expander("⚙️ Admin Settings", expanded=True):
        st.markdown("### Manage Settings")

        # Add Vehicle
        vehicle_name = st.text_input("Add Vehicle")
        if st.button("Add Vehicle"):
            if vehicle_name:
                settings["vehicles"].append(vehicle_name)
                st.success(f"✅ Added vehicle: {vehicle_name}")

        # Add Circuit
        circuit_name = st.text_input("Add Collection Circuit")
        if st.button("Add Circuit"):
            if circuit_name:
                settings["circuits"].append(circuit_name)
                st.success(f"✅ Added circuit: {circuit_name}")

        # Add Employee
        employee_name = st.text_input("Add Employee")
        if st.button("Add Employee"):
            st.success(f"✅ Added employee: {employee_name} (just visual for now)")

    st.sidebar.markdown("---")
    st.sidebar.caption("© 2025 WasteTrack")

