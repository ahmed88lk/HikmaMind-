import streamlit as st
from utils.config import ANALOGY_STYLES, FIELDS, KNOWLEDGE_LEVELS
from models.user_profile import UserProfile, save_profile, get_current_profile

def render_header():
    """Display application header"""
    st.title("🧠 HikmaMind")
    st.subheader("Transform complex concepts into easy-to-understand analogies")
    
    st.markdown("""
    This app uses AI to help professionals and researchers understand 
    research papers or YouTube videos by creating simple analogies 
    and clear summaries tailored to your learning style.
    """)

def render_about():
    """Display About section"""
    st.markdown("---")
    st.markdown("""
    ### About HikmaMind

    HikmaMind is designed to help IT professionals and researchers quickly understand 
    complex concepts through AI-generated analogies and summaries personalized to your profile.

    **Technologies used:**
    - Streamlit for the user interface
    - Google Gemini AI for content analysis
    - Support for YouTube videos and PDF documents
    
    **How it works:**
    1. Complete your learning profile
    2. Submit a video or document
    3. Get explanations tailored to your level and style
    """)

def render_sidebar():
    """Display and manage user profile in sidebar"""
    st.sidebar.title("Your Learning Profile")
    
    # Get current profile
    current_profile = get_current_profile()
    
    # Form to update profile
    with st.sidebar.form("user_profile_form"):
        st.subheader("Customize Your Explanations")
        
        field = st.selectbox(
            "Your field of expertise",
            options=FIELDS,
            index=FIELDS.index(current_profile.field) if current_profile.field in FIELDS else 0
        )
        
        knowledge_level = st.radio(
            "Your knowledge level",
            options=KNOWLEDGE_LEVELS,
            index=KNOWLEDGE_LEVELS.index(current_profile.knowledge_level) if current_profile.knowledge_level in KNOWLEDGE_LEVELS else 0,
            help="This helps us adjust the detail and jargon level"
        )
        
        analogy_style = st.selectbox(
            "Preferred analogy style",
            options=list(ANALOGY_STYLES.keys()),
            index=list(ANALOGY_STYLES.keys()).index(current_profile.analogy_style) if current_profile.analogy_style in ANALOGY_STYLES else 0,
            help="Choose the type of analogies that works best for you"
        )
        
        include_citations = st.checkbox(
            "Include citations/references",
            value=current_profile.include_citations,
            help="Add references to original sources"
        )
        
        submitted = st.form_submit_button("Save My Profile")
        
        if submitted:
            # Update profile
            updated_profile = UserProfile(
                field=field,
                knowledge_level=knowledge_level,
                analogy_style=analogy_style,
                include_citations=include_citations
            )
            save_profile(updated_profile)
            st.sidebar.success("✅ Profile saved successfully!")
            return updated_profile
    
    # Display profile summary
    if current_profile.is_complete():
        st.sidebar.markdown("---")
        st.sidebar.subheader("Your Profile Summary")
        st.sidebar.markdown(f"""
        - **Field:** {current_profile.field}
        - **Level:** {current_profile.knowledge_level}
        - **Analogy style:** {current_profile.analogy_style}
        - **Citations:** {"Yes" if current_profile.include_citations else "No"}
        """)
    
    return current_profile
