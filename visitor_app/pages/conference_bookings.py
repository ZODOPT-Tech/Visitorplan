# pages/conference_booking.py
import streamlit as st
from utils.helpers import nav

def app():
    st.markdown("<div class='header-box'>CONFERENCE BOOKING</div>", unsafe_allow_html=True)
    name = st.text_input("Your name")
    date = st.date_input("Date")
    start = st.time_input("Start time")
    end = st.time_input("End time")
    if st.button("Book", use_container_width=True):
        st.success("Booked! (Demo)")
    if st.button("Back to Home"):
        nav("home")
