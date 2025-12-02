# pages/home.py
import streamlit as st
from utils.helpers import nav
from pathlib import Path

def app():
    # --- Header (Keep as is, but ensure assets/zodopt.png exists) ---
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; background-color: #5500ff; padding: 10px 20px; border-radius: 8px;">
      <div style="font-size:36px; font-weight:800; color:white;">ZODOPT MEETEASE</div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        display:flex; 
        justify-content:space-between; 
        align-items:center; 
        background-color: #5500ff; 
        padding: 10px 20px; 
        border-radius: 8px;
        margin-top: -10px; /* Adjust to sit right below the main header */
    ">
      <div style="font-size:36px; font-weight:800; color:white;">ZODOPT MEETEASE</div>
      <img src="https://i.imgur.com/KxS1Y7d.png" style='width:120px; height:auto; border-radius:8px;'/>
    </div>
    """, unsafe_allow_html=True) # Used an external URL placeholder for the Zodopt logo
    st.write("")
    st.write("")

    col1, col2 = st.columns(2)
    
    # --- Card 1: Visit Plan ---
    with col1:
        # The Card Body (The Icon)
        # Replicating the purple circle icon on a white card background.
        st.markdown("""
        <div style='
            background-color: white; 
            border-radius: 12px 12px 0 0; /* Rounded top corners, straight bottom */
            padding: 40px 28px; 
            height: 250px; /* Give it a fixed height for visual balance */
            display: flex; 
            justify-content: center; 
            align-items: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.06); /* subtle shadow */
        '>
          <div style='
            background-color: #7f50ff; /* Purple gradient/color from image */
            width: 150px; 
            height: 150px; 
            border-radius: 50%; 
            display: flex; 
            justify-content: center; 
            align-items: center;
          '>
            <img src='https://img.icons8.com/color/100/ffffff/calendar--v1.png' style='width: 80px; height: 80px;'/>
          </div>
        </div>
        """, unsafe_allow_html=True)
        
        # The Button (The Label 'Visit Plan')
        # Overriding the default Streamlit button style to match the solid blue bar
        st.markdown("""
        <style>
        div[data-testid="column"]:nth-child(1) .stButton > button {
            background-color: #2563eb; /* Solid Blue */
            color: white; 
            font-size: 18px; 
            font-weight: 600;
            padding: 15px 0;
            border-radius: 0 0 12px 12px; /* Rounded bottom corners */
            border: none;
            margin-top: -3px; /* Pull up to touch the card body */
        }
        </style>
        """, unsafe_allow_html=True)
        
        # NOTE: The button text 'Visit Plan' is now the label on the blue bar.
        if st.button("Visit Plan", key="open_visitplan", use_container_width=True):
            nav("visitplan_login")

    # --- Card 2: Conference Booking ---
    with col2:
        # The Card Body (The Icon)
        # Replicating the green circle icon on a white card background.
        st.markdown("""
        <div style='
            background-color: white; 
            border-radius: 12px 12px 0 0; 
            padding: 40px 28px; 
            height: 250px;
            display: flex; 
            justify-content: center; 
            align-items: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.06); 
        '>
          <div style='
            background-color: #10b981; /* Green color from image */
            width: 150px; 
            height: 150px; 
            border-radius: 50%; 
            display: flex; 
            justify-content: center; 
            align-items: center;
          '>
            <img src='https://img.icons8.com/color/100/ffffff/book.png' style='width: 80px; height: 80px;'/>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # The Button (The Label 'Conference Booking')
        # Overriding the default Streamlit button style for the second column
        st.markdown("""
        <style>
        div[data-testid="column"]:nth-child(2) .stButton > button {
            background-color: #2563eb; /* Solid Blue */
            color: white; 
            font-size: 18px; 
            font-weight: 600;
            padding: 15px 0;
            border-radius: 0 0 12px 12px; 
            border: none;
            margin-top: -3px; 
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("Conference Booking", key="open_conf", use_container_width=True):
            nav("conference_booking")

if __name__ == "__main__":
    app()
