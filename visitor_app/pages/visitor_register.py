# pages/visitor_register.py
import streamlit as st
from utils.helpers import nav
from utils.aws_db import get_connection

def app():
    user = st.session_state.get("user")
    if not user:
        st.warning("Please login first.")
        nav("visitplan_login")
        return

    st.markdown("<div class='header-box'>VISITOR REGISTRATION — PRIMARY DETAILS</div>", unsafe_allow_html=True)
    name = st.text_input("Full Name", key="r_name")
    phone = st.text_input("Phone", key="r_phone")
    email = st.text_input("Email", key="r_email")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next → Identity", use_container_width=True):
            if not name.strip():
                st.error("Name required")
                return
            # create visitor master row
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO visitors (full_name, email, phone, company_id) VALUES (%s,%s,%s,%s)",
                        (name.strip(), email.strip(), phone.strip(), user["company_id"]))
            conn.commit()
            visitor_id = cur.lastrowid
            cur.close()
            # save in session
            st.session_state.visitor = {"id": visitor_id, "name": name.strip(), "email": email.strip(), "phone": phone.strip()}
            nav("visitor_identity")
    with col2:
        if st.button("Cancel", use_container_width=True):
            nav("visitplan_admin_dashboard")
