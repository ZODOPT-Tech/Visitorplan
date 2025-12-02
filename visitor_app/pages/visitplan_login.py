# pages/visitplan_login.py
import streamlit as st
from utils.helpers import nav
from utils.auth import admin_login, create_admin, get_admin_by_email
from utils.aws_db import init_db

def app():
    init_db()  # create tables if not exist
    st.markdown("<div class='header-box'>VISITOR ADMIN LOGIN</div>", unsafe_allow_html=True)
    st.write("")
    email = st.text_input("Admin Email", key="admin_login_email")
    pwd = st.text_input("Password", type="password", key="admin_login_pwd")

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("Login", use_container_width=True):
            admin = admin_login(email.strip(), pwd.strip())
            if admin:
                # set session user
                st.session_state.user = {"admin_id": admin["id"], "admin_email": admin["email"], "company_id": admin["company_id"]}
                nav("visitplan_admin_dashboard")
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("New Registration (Admin)", use_container_width=True):
            nav("admin_register")

    with col3:
        if st.button("Forgot Password", use_container_width=True):
            nav("forgot_password")
