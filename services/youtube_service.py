import streamlit as st
from google import genai
from models.user_profile import UserProfile

def generate_prompt_for_youtube(analogy_type, user_profile):
    """Generate a simple English prompt string based on analysis type and user profile."""
    if analogy_type == "Simple summary (3 sentences)":
        base_prompt = "Please summarize this video in 3 sentences."
    elif analogy_type == "Detailed analogy":
        base_prompt = "Explain the key concepts of this video using simple, familiar analogies."
    elif analogy_type == "Key points":
        base_prompt = "List and explain the 5 key points of this video."
    else:  # Beginner explanation
        base_prompt = "Explain the content of this video as if presenting to someone new to the topic."
    
    profile_context = (
        f"The user is in the field of {user_profile.field}, "
        f"knowledge level: {user_profile.knowledge_level}, "
        f"prefers analogies: {user_profile.analogy_style}."
    )
    
    prompt = f"{profile_context}\n{base_prompt}"
    return prompt

def youtube_analyzer(client, user_profile: UserProfile):
    st.header("YouTube Video Analysis")
    
    yt_url = st.text_input(
        "Enter a YouTube video URL:",
        help="Example: https://www.youtube.com/watch?v=9hE5-98ZeCg"
    )
    
    analogy_type = st.selectbox(
        "Type of analysis:",
        ["Simple summary (3 sentences)", "Detailed analogy", "Key points", "Beginner explanation"]
    )
    
    if st.button("Analyze video"):
        if yt_url:
            try:
                with st.spinner("Analyzing video..."):
                    prompt = generate_prompt_for_youtube(analogy_type, user_profile)
                    
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-preview-04-17",
                        contents=genai.types.Content(
                            parts=[
                                genai.types.Part(
                                    file_data=genai.types.FileData(file_uri=yt_url)
                                ),
                                genai.types.Part(text=prompt)
                            ]
                        )
                    )
                    
                    st.success("Analysis complete!")
                    
                    with st.container(border=True):
                        st.subheader("🎯 Personalized analysis for your profile")
                        st.caption(f"Field: {user_profile.field} | Level: {user_profile.knowledge_level} | Analogy style: {user_profile.analogy_style}")
                        st.markdown(response.text)
                    
                    st.markdown("### Your feedback helps us improve")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("👍 Very helpful"):
                            st.toast("Thank you for your positive feedback!")
                    with col2:
                        if st.button("😐 Somewhat helpful"):
                            st.toast("Thanks for your feedback! We'll work to improve.")
                    with col3:
                        if st.button("👎 Not helpful"):
                            st.toast("Sorry this wasn't helpful. We'll improve!")
                            st.text_area("What wasn't helpful?", placeholder="Your comments help us improve...")
                    
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
        else:
            st.warning("⚠️ Please enter a valid YouTube URL.")
