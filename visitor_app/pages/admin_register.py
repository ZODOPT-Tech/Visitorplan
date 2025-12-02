# pages/admin_register.py
import streamlit as st
from utils.helpers import nav
from utils.auth import create_admin, get_admin_by_email

def app():
    st.markdown("<div class='header-box'>CREATE ADMIN</div>", unsafe_allow_html=True)
    st.write("")
    name = st.text_input("Full Name", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    company = st.text_input("Company", key="reg_company")
    pwd = st.text_input("Password", type="password", key="reg_pwd")
    cpwd = st.text_input("Confirm Password", type="password", key="reg_cpwd")

    if st.button("Create Admin", use_container_width=True):
        if not (name and email and company and pwd and cpwd):
            st.error("Please fill all fields")
        elif pwd != cpwd:
            st.error("Password and Confirm Password do not match")
        elif get_admin_by_email(email.strip()):
            st.error("Admin with this email already exists")
        else:
            create_admin(name.strip(), email.strip(), pwd.strip(), company_name=company.strip())
            st.success("Admin created. Login now.")
            nav("visitplan_login")
    if st.button("Back to Login", use_container_width=True):
        nav("visitplan_login")
