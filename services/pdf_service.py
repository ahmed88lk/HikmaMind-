import streamlit as st
import httpx
from google import genai
from models.user_profile import UserProfile
from utils.config import generate_image
from PIL import Image
from io import BytesIO

def generate_prompt_for_pdf(analysis_type, user_profile):
    """Generate a simple prompt string based on analysis type and user profile."""
    if analysis_type == "General summary":
        base_prompt = "Summarize this research paper concisely."
    elif analysis_type == "Detailed analogy":
        base_prompt = "Explain the main concepts of this paper using simple, familiar analogies."
    elif analysis_type == "Simplify concepts":
        base_prompt = "Simplify the complex concepts in this paper for a non-expert audience."
    else:  # Key research points
        base_prompt = "Identify and explain the main contributions and key findings of this research."
    # Add user profile context
    profile_context = (
        f"The user is in the field of {user_profile.field}, "
        f"knowledge level: {user_profile.knowledge_level}, "
        f"prefers analogies: {user_profile.analogy_style}."
    )
    prompt = f"{profile_context}\n{base_prompt}"
    return prompt

def pdf_url_analyzer(client, user_profile: UserProfile):
    st.header("Analyze PDF from URL")
    pdf_url = st.text_input(
        "Enter the URL of a PDF document:",
        help="Example: https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"
    )
    pdf_analogy_type = st.selectbox(
        "Type of analysis:",
        ["General summary", "Detailed analogy", "Simplify concepts", "Key research points"],
        key="pdf_url_analogy"
    )
    if st.button("Analyze PDF", key="analyze_pdf_url"):
        if pdf_url:
            try:
                with st.spinner("Downloading and analyzing PDF..."):
                    doc_data = httpx.get(pdf_url).content
                    prompt = generate_prompt_for_pdf(pdf_analogy_type, user_profile)
                    # Use Gemini 2.5 model, pass PDF as bytes and prompt as string
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-preview-04-17",
                        contents=[
                            genai.types.Part.from_bytes(
                                data=doc_data,
                                mime_type='application/pdf',
                            ),
                            prompt
                        ]
                    )
                    st.success("Analysis complete!")
                    st.subheader("Personalized analysis")
                    st.caption(f"Field: {user_profile.field} | Level: {user_profile.knowledge_level} | Analogy style: {user_profile.analogy_style}")
                    st.markdown(response.text)
                    st.download_button(
                        label="Download analysis as TXT",
                        data=response.text,
                        file_name="hikmamind_analysis.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
        else:
            st.warning("Please enter a valid PDF URL.")

    # Add image generation option
    with st.expander("Generate images to illustrate concepts"):
        st.info("You can generate images to help visualize complex concepts from the paper")
        image_prompt = st.text_area("Describe the image you want to generate:", 
                                  placeholder="E.g., Create a visual representation of neural networks as described in this paper")
        
        if st.button("Generate Image", key="generate_img_url") and image_prompt:
            try:
                with st.spinner("Generating image..."):
                    text_response, image_data = generate_image(client, image_prompt)
                    
                    if image_data:
                        st.image(Image.open(BytesIO(image_data)), caption="Generated Image")
                        st.download_button(
                            label="Download Image",
                            data=BytesIO(image_data).getvalue(),
                            file_name="hikmamind_generated_image.png",
                            mime="image/png"
                        )
                    if text_response:
                        st.write("AI comments on the image:")
                        st.write(text_response)
            except Exception as e:
                st.error(f"Error generating image: {str(e)}")

def pdf_upload_analyzer(client, user_profile: UserProfile):
    st.header("Analyze uploaded PDF")
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
    pdf_upload_analogy_type = st.selectbox(
        "Type of analysis:",
        ["General summary", "Detailed analogy", "Simplify concepts", "Key research points"],
        key="pdf_upload_analogy"
    )
    if st.button("Analyze PDF", key="analyze_pdf_upload") and uploaded_file is not None:
        try:
            with st.spinner("Analyzing PDF..."):
                pdf_data = uploaded_file.getvalue()
                prompt = generate_prompt_for_pdf(pdf_upload_analogy_type, user_profile)
                response = client.models.generate_content(
                    model="gemini-2.5-flash-preview-04-17",
                    contents=[
                        genai.types.Part.from_bytes(
                            data=pdf_data,
                            mime_type='application/pdf',
                        ),
                        prompt
                    ]
                )
                st.success("Analysis complete!")
                st.subheader("Personalized analysis")
                st.caption(f"Field: {user_profile.field} | Level: {user_profile.knowledge_level} | Analogy style: {user_profile.analogy_style}")
                st.markdown(response.text)
                st.download_button(
                    label="Download analysis as TXT",
                    data=response.text,
                    file_name=f"hikmamind_analysis_{uploaded_file.name.split('.')[0]}.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

    # Add image generation option
    with st.expander("Generate images to illustrate concepts"):
        st.info("You can generate images to help visualize complex concepts from the paper")
        image_prompt = st.text_area("Describe the image you want to generate:", 
                                  placeholder="E.g., Create a visual representation of neural networks as described in this paper",
                                  key="img_prompt_upload")
        
        if st.button("Generate Image", key="generate_img_upload") and image_prompt:
            try:
                with st.spinner("Generating image..."):
                    text_response, image_data = generate_image(client, image_prompt)
                    
                    if image_data:
                        st.image(Image.open(BytesIO(image_data)), caption="Generated Image")
                        st.download_button(
                            label="Download Image",
                            data=BytesIO(image_data).getvalue(),
                            file_name="hikmamind_generated_image.png",
                            mime="image/png"
                        )
                    if text_response:
                        st.write("AI comments on the image:")
                        st.write(text_response)
            except Exception as e:
                st.error(f"Error generating image: {str(e)}")
