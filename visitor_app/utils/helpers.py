# utils/helpers.py
import streamlit as st

def init_nav():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "user" not in st.session_state:
        st.session_state.user = None
    if "visitor" not in st.session_state:
        st.session_state.visitor = None

def nav(page_name: str):
    st.session_state.page = page_name
    st.rerun()

def logout():
    st.session_state.clear()
    init_nav()
    st.rerun()
