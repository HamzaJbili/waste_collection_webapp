# auth.py

import streamlit as st
import hashlib
import json
import os
from config import CREDENTIALS_FILE

# --- Load or define users ---
def load_users():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    # Return default admin if file not found
    return {"admin": hashlib.sha256("admin123".encode()).hexdigest()}

# --- Save users back to file ---
def save_users(users_dict):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(users_dict, file)

# --- Define globally loaded users for access across functions ---
users = load_users()

# --- Return current user dict ---
def get_users():
    return users

# --- Authenticate a login attempt ---
def login(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return users.get(username) == hashed

# --- Initialize session state on startup ---
def init_session():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

# --- UI for login screen ---
def login_user():
    st.image("https://i.imgur.com/fxyD8rF.png", width=140)
    st.markdown("## 🌍 WasteTrack: Intelligent Waste Collection")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("🔐 Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful. Redirecting...")
            st.rerun()
        else:
            st.error("Invalid credentials")
