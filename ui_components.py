import streamlit as st

def apply_styling():
    st.markdown("""
        <style>
        body {
            background: linear-gradient(to right, #f7fff7, #e3f6f5);
        }
        button[kind="primary"] {
            background-color: #38b000 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1) !important;
        }
        </style>
    """, unsafe_allow_html=True)

def show_logo_title():
    st.markdown("""
        <div style="padding: 1.5rem; background: linear-gradient(90deg, #d3f9d8, #b2f7ef); 
                    border-radius: 1rem; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: #2b9348; font-size: 2.5rem; font-weight: bold;">
                🚛 WasteTrack: Smart Waste Collection
            </h1>
            <p style="font-size: 1.1rem; color: #444;">
                Your streamlined, eco-friendly waste management SaaS solution.
            </p>
        </div>
    """, unsafe_allow_html=True)

def show_sidebar(settings):
    st.sidebar.markdown("### 👤 User Panel")
    st.sidebar.info(f"👋 Logged in as: `{st.session_state.username}`")

    st.sidebar.markdown("#### 🚧 Admin Settings")
    st.sidebar.markdown("""
        <div style="padding: 1rem; background: #ffffffdd; border-radius: 1rem;">
    """, unsafe_allow_html=True)

    vehicle = st.sidebar.text_input("Add Vehicle")
    if st.sidebar.button("Add Vehicle") and vehicle:
        settings["vehicles"].append(vehicle)

    circuit = st.sidebar.text_input("Add Collection Circuit")
    if st.sidebar.button("Add Circuit") and circuit:
        settings["circuits"].append(circuit)

    employee = st.sidebar.text_input("Add Employee")
    if st.sidebar.button("Add Employee") and employee:
        settings["employees"].append(employee)

    st.sidebar.markdown("</div>", unsafe_allow_html=True)
