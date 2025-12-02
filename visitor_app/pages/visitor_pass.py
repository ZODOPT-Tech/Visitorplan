# pages/visitor_pass.py
import streamlit as st
from utils.helpers import nav
from utils.aws_db import get_connection
import qrcode
from io import BytesIO
import base64

def make_qr(data: str):
    img = qrcode.make(data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def app():
    visitor = st.session_state.get("visitor")
    if not visitor:
        st.warning("No visitor data; start registration")
        nav("visitor_register")
        return
    st.markdown("<div class='header-box'>VISITOR PASS</div>", unsafe_allow_html=True)
    st.write("")
    st.markdown(f"**Name:** {visitor.get('name')}")
    st.markdown(f"**Phone:** {visitor.get('phone')}")
    st.markdown(f"**Email:** {visitor.get('email')}")
    # generate QR with visitor id and timestamp
    payload = f"visitor:{visitor.get('id')}|company:{st.session_state.user['company_id'] if st.session_state.get('user') else '0'}"
    buf = make_qr(payload)
    st.image(buf)
    # provide downloadable PNG
    b64 = base64.b64encode(buf.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="visitor_pass.png">Download Pass (PNG)</a>'
    st.markdown(href, unsafe_allow_html=True)
    if st.button("Back to Dashboard"):
        nav("visitplan_admin_dashboard")
