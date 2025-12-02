# pages/visitplan_admin_dashboard.py
import streamlit as st
from utils.helpers import nav, logout
from utils.aws_db import get_connection
import pandas as pd

def app():
    user = st.session_state.get("user")
    if not user:
        st.warning("Please login first.")
        nav("visitplan_login")
        return
    st.markdown("<div class='header-box'>ADMIN DASHBOARD</div>", unsafe_allow_html=True)
    st.write(f"Logged in as: {user['admin_email']}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register New Visitor", use_container_width=True):
            nav("visitor_register")
        if st.button("Visitor List", use_container_width=True):
            nav("visitor_list")
    with col2:
        if st.button("Generate Pass", use_container_width=True):
            nav("visitor_pass")
        if st.button("Logout", use_container_width=True):
            logout()
    st.markdown("### Recent visitors")
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT v.id, v.full_name, v.email, v.phone, vd.visit_type, vd.person_to_meet, vd.created_at FROM visitors v LEFT JOIN visitor_details vd ON vd.visitor_id=v.id WHERE v.company_id=%s ORDER BY v.id DESC LIMIT 10", (user["company_id"],))
    rows = cur.fetchall()
    cur.close()
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df)
    else:
        st.info("No visitors yet.")
