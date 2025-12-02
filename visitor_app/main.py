import streamlit as st
from utils.helpers import nav # Import the navigation helper

def app():
    """Renders the home page with the header and two feature cards."""

    # 1. Container for the entire content area, applying the box-shadow and background
    with st.container(border=False):
        # We need to use HTML to create the wrapper div for our custom styling
        st.markdown('<div class="container-box">', unsafe_allow_html=True)

        # 2. Header Bar (Zodopt Meetease)
        # Using custom CSS classes for the gradient and layout
        st.markdown(
            f"""
            <div class="header-bar">
                <h1>ZODOPT MEETEASE</h1>
                <div class="header-logo-text">
                    ZOD<span class="red">o</span>p<span class="green">t</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 3. Feature Cards Container (Visit Plan & Conference Booking)
        st.markdown('<div class="feature-cards-container">', unsafe_allow_html=True)

        # --- Card 1: Visit Plan ---
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        
        # Use a Streamlit column for alignment and centering (inside the custom HTML)
        col_content = st.columns([1])[0]
        with col_content:
            # Placeholder for the icon (using a div for the circle background)
            # You'll need to define CSS for .icon-calendar-bg and .icon-calendar to match the image
            st.markdown(
                """
                <div style="padding: 25px 20px 0; text-align: center;">
                    <!-- Placeholder for Calendar Icon - Requires custom CSS for colors -->
                    <div style="
                        width: 100px; 
                        height: 100px; 
                        border-radius: 50%; 
                        background: linear-gradient(135deg, #a77dff, #5c62ec); 
                        display: inline-flex; 
                        justify-content: center; 
                        align-items: center; 
                        margin-bottom: 20px;">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 50px; height: 50px;">
                          <rect x="5" y="6" width="14" height="13" rx="2" fill="#fff" opacity="0.8"/>
                          <rect x="5" y="6" width="14" height="3" rx="0" fill="#fff" opacity="0.9"/>
                          <path d="M9 10H7V12H9V10Z" fill="#a77dff"/>
                          <path d="M12 10H10V12H12V10Z" fill="#a77dff"/>
                          <path d="M15 10H13V12H15V10Z" fill="#a77dff"/>
                          <path d="M9 13H7V15H9V13Z" fill="#a77dff"/>
                          <path d="M12 13H10V15H12V13Z" fill="#a77dff"/>
                          <path d="M15 13H13V15H15V13Z" fill="#a77dff"/>
                        </svg>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )

            # Button is created using st.button which is styled by the CSS
            if st.button("Visit Plan", key="visit_plan_btn"):
                nav("visitplan_login") # Use the helper function for navigation
                
        st.markdown('</div>', unsafe_allow_html=True) # close feature-card

        # --- Card 2: Conference Booking ---
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        
        col_content_2 = st.columns([1])[0]
        with col_content_2:
            # Placeholder for the icon (using a div for the circle background)
            st.markdown(
                """
                <div style="padding: 25px 20px 0; text-align: center;">
                    <!-- Placeholder for Conference Icon - Requires custom CSS for colors -->
                    <div style="
                        width: 100px; 
                        height: 100px; 
                        border-radius: 50%; 
                        background: #34c759; 
                        display: inline-flex; 
                        justify-content: center; 
                        align-items: center; 
                        margin-bottom: 20px;">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 50px; height: 50px;">
                          <rect x="7" y="5" width="10" height="14" rx="1" fill="#fff" opacity="0.9"/>
                          <rect x="7" y="16" width="10" height="3" rx="0" fill="#4338ca"/>
                        </svg>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("Conference Booking", key="conference_booking_btn"):
                nav("conference_booking") # Use the helper function for navigation

        st.markdown('</div>', unsafe_allow_html=True) # close feature-card

        st.markdown('</div>', unsafe_allow_html=True) # close feature-cards-container

        st.markdown('</div>', unsafe_allow_html=True) # close container-box
        
# Set a default page if the file is run directly (useful for testing)
if __name__ == "__main__":
    app()
