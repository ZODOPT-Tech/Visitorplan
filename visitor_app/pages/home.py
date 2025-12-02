# pages/home.py
import streamlit as st
from utils.helpers import nav
from pathlib import Path

def app():
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div style="font-size:36px; font-weight:800; color:white; padding:14px;">ZODOPT MEETEASE</div>
      <img src='assets/zodopt.png' style='width:120px; height:auto; border-radius:8px;'/>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='big-card' style='padding:28px;'>
          <div style='display:flex; justify-content:center;'><img src='https://img.icons8.com/ios-filled/100/ffffff/planner.png'/></div>
          <h2 style='text-align:center; color:#111827;'>VISITPLAN</h2>
          <p style='text-align:center; color:#6b7280;'>Register and manage visitors</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open VISITPLAN", key="open_visitplan", use_container_width=True):
            nav("visitplan_login")
    with col2:
        st.markdown("""
        <div class='big-card' style='padding:28px;'>
          <div style='display:flex; justify-content:center;'><img src='https://img.icons8.com/ios-filled/100/ffffff/book.png'/></div>
          <h2 style='text-align:center; color:#111827;'>CONFERENCE BOOKING</h2>
          <p style='text-align:center; color:#6b7280;'>Reserve conference rooms</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open CONFERENCE BOOKING", key="open_conf", use_container_width=True):
            nav("conference_booking")
