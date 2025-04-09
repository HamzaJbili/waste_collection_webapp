# auth.py

import streamlit as st
import hashlib
import json
import os
from config import CREDENTIALS_FILE

def load_users():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {"admin": hashlib.sha256("admin123".encode()).hexdigest()}

def save_users(users):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(users, file)

def login(username, password):
    users = load_users()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return users.get(username) == hashed

def init_session():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

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
