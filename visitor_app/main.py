# main.py
import streamlit as st
from utils.helpers import init_nav
from pathlib import Path

# page config & load css
st.set_page_config(page_title="Zodopt Meetease", layout="wide", initial_sidebar_state="collapsed")
css_path = Path("styles.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# init session navigation
init_nav()

# router
page = st.session_state.get("page", "home")
# mapping
ROUTES = {
    "home": "pages.home",
    "visitplan_login": "pages.visitplan_login",
    "visitplan_admin_dashboard": "pages.visitplan_admin_dashboard",
    "visitor_register": "pages.visitor_register",
    "visitor_identity": "pages.visitor_identity",
    "visitor_details": "pages.visitor_details",
    "visitor_pass": "pages.visitor_pass",
    "conference_booking": "pages.conference_booking",
    "admin_register": "pages.admin_register",
    "forgot_password": "pages.forgot_password",
    "visitor_list": "pages.visitor_list"
}

# dynamic import and call app()
module = ROUTES.get(page, "pages.home")
mod = __import__(module, fromlist=["app"])
mod.app()
