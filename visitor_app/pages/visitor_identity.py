# pages/visitor_identity.py
import streamlit as st
from utils.helpers import nav
from utils.aws_db import get_connection

def app():
    if not st.session_state.get("visitor"):
        st.warning("Start registration first")
        nav("visitor_register")
        return
    st.markdown("<div class='header-box'>VISITOR IDENTITY</div>", unsafe_allow_html=True)
    vid = st.session_state.visitor["id"]
    id_type = st.selectbox("ID Type", ["Aadhaar", "PAN", "Driving License", "Passport"], key="id_type")
    id_number = st.text_input("ID Number", key="id_number")
    id_file = st.file_uploader("Upload ID Proof (image/pdf)", type=["png","jpg","jpeg","pdf"], key="id_file")
    photo = st.camera_input("Capture Photo (use camera) - optional")
    if st.button("Next → Details", use_container_width=True):
        # save identity
        id_blob = id_file.getvalue() if id_file else None
        photo_blob = photo.getvalue() if photo else None
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO visitor_identity (visitor_id, id_type, id_number, id_image, visitor_photo) VALUES (%s,%s,%s,%s,%s)",
                    (vid, id_type, id_number.strip() or None, id_blob, photo_blob))
        conn.commit()
        cur.close()
        nav("visitor_details")
    if st.button("Back", use_container_width=True):
        nav("visitor_register")
