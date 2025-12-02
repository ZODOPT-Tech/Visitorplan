# pages/forgot_password.py
import streamlit as st
from utils.helpers import nav
from utils.auth import get_admin_by_email, reset_admin_password

def app():
    st.markdown("<div class='header-box'>FORGOT PASSWORD</div>", unsafe_allow_html=True)
    st.write("")
    email = st.text_input("Enter your admin email", key="fp_email")
    if st.button("Verify Email", use_container_width=True):
        admin = get_admin_by_email(email.strip())
        if not admin:
            st.error("No admin with this email")
        else:
            st.session_state.fp_email = email.strip()
            st.success("Email verified. Enter new password below.")
    if st.session_state.get("fp_email"):
        newp = st.text_input("New password", type="password", key="fp_new")
        cp = st.text_input("Confirm new password", type="password", key="fp_cnew")
        if st.button("Reset Password", use_container_width=True):
            if newp != cp:
                st.error("Passwords do not match")
            else:
                reset_admin_password(st.session_state.fp_email, newp)
                st.success("Password reset successful. Please login.")
                nav("visitplan_login")
    if st.button("Back to Login", use_container_width=True):
        nav("visitplan_login")
