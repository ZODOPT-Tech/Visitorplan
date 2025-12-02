# pages/visitor_details.py
import streamlit as st
from utils.helpers import nav
from utils.aws_db import get_connection
from io import BytesIO

# optional canvas
try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS = True
except Exception:
    CANVAS = False

def app():
    if not st.session_state.get("visitor"):
        st.warning("Start registration first")
        nav("visitor_register")
        return
    st.markdown("<div class='header-box'>VISITOR DETAILS — SECONDARY</div>", unsafe_allow_html=True)
    vid = st.session_state.visitor["id"]

    visit_type = st.selectbox("Visit Type", ["One-time", "Recurring", "Contractor", "Delivery", "Other"], key="vd_visit_type")
    from_company = st.text_input("From Company", key="vd_from_company")
    department = st.text_input("Department", key="vd_department")
    designation = st.text_input("Designation", key="vd_designation")
    org_address = st.text_area("Organization Address", key="vd_org_address")
    addr1 = st.text_input("Address Line 1", key="vd_addr1")
    city = st.text_input("City / District", key="vd_city")
    state = st.text_input("State / Province", key="vd_state")
    postal = st.text_input("Postal Code", key="vd_postal")
    country = st.text_input("Country", value="India", key="vd_country")
    gender = st.radio("Gender", ["Male","Female","Others"], key="vd_gender")
    purpose = st.text_area("Purpose", key="vd_purpose")
    person_to_meet = st.text_input("Person to Meet", key="vd_person")
    st.markdown("**Belongings**")
    bags = st.checkbox("Bags", key="vd_bags")
    docs = st.checkbox("Documents", key="vd_docs")
    elec = st.checkbox("Electronic Items", key="vd_elec")
    laptop = st.checkbox("Laptop", key="vd_laptop")
    charger = st.checkbox("Charger", key="vd_charger")
    powerbank = st.checkbox("Power Bank", key="vd_powerbank")

    st.markdown("---")
    st.info("Capture signature (draw) or upload image.")
    signature_blob = None
    if CANVAS:
        canvas_result = st_canvas(stroke_width=2, stroke_color="#ffffff", background_color="#0b1020", height=180, width=800, key="sig_canvas")
        if canvas_result and canvas_result.image_data is not None:
            from PIL import Image
            import numpy as np
            arr = (canvas_result.image_data * 255).astype("uint8")
            img = Image.fromarray(arr)
            buf = BytesIO()
            img.save(buf, format="PNG")
            signature_blob = buf.getvalue()
            st.image(signature_blob, caption="Signature preview", width=250)
    else:
        sig_file = st.file_uploader("Upload signature image (png/jpg)", type=["png","jpg","jpeg"], key="sig_upload")
        if sig_file:
            signature_blob = sig_file.getvalue()
            st.image(signature_blob, caption="Signature preview", width=250)

    if st.button("Submit & Finish", use_container_width=True):
        belongings = ",".join([b for b,v in [("Bags",bags),("Documents",docs),("Electronic Items",elec),("Laptop",laptop),("Charger",charger),("Power Bank",powerbank)] if v])
        # optional visitor photo already in visitor_identity; we don't require photo here
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO visitor_details (visitor_id, visit_type, from_company, department, designation, organization_address, address_line1,
            city, state, postal_code, country, gender, purpose, person_to_meet, belongings, photo_blob, signature_blob)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (vid, visit_type, from_company, department, designation, org_address, addr1, city, state, postal, country, gender, purpose, person_to_meet, belongings, None, signature_blob))
        conn.commit()
        cur.close()
        st.success("Visitor details saved.")
        nav("visitor_pass")
    if st.button("Back", use_container_width=True):
        nav("visitor_identity")
