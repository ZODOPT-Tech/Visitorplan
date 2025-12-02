# pages/visitor_list.py
import streamlit as st
from utils.aws_db import get_connection
from utils.helpers import nav
import pandas as pd

def app():
    user = st.session_state.get("user")
    if not user:
        st.warning("Please login")
        nav("visitplan_login")
        return
    st.markdown("<div class='header-box'>VISITOR LIST</div>", unsafe_allow_html=True)
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT v.id, v.full_name, v.phone, v.email, vd.visit_type, vd.person_to_meet, vd.created_at FROM visitors v LEFT JOIN visitor_details vd ON vd.visitor_id=v.id WHERE v.company_id=%s ORDER BY v.id DESC", (user["company_id"],))
    rows = cur.fetchall()
    cur.close()
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df)
    else:
        st.info("No visitors.")
    if st.button("Back"):
        nav("visitplan_admin_dashboard")
