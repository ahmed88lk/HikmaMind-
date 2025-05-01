import streamlit as st
from utils.config import configure_api
from utils.ui_components import render_header, render_about, render_sidebar
from services.youtube_service import youtube_analyzer
from services.pdf_service import pdf_url_analyzer, pdf_upload_analyzer
from models.user_profile import save_profile, get_current_profile, initialize_session_state

# Page and API config
st.set_page_config(
    page_title="HikmaMind - AI Research Assistant",
    page_icon="🧠",
    layout="wide"
)

# API configuration
client = configure_api()
if client is None:
    st.error("API key not found. Please configure the GOOGLE_GENAI_API_KEY environment variable.")
    st.stop()

# Initialize session state
initialize_session_state()

# Render header
render_header()

# User profile in sidebar
user_profile = render_sidebar()

# Main interface
if not user_profile.is_complete():
    st.info("👋 Please complete your profile to continue")
else:
    tab1, tab2, tab3 = st.tabs([
        "Analyze YouTube Video", 
        "Analyze PDF from URL", 
        "Analyze Uploaded PDF"
    ])

    with tab1:
        youtube_analyzer(client, user_profile)

    with tab2:
        pdf_url_analyzer(client, user_profile)

    with tab3:
        pdf_upload_analyzer(client, user_profile)

# About section
render_about()
