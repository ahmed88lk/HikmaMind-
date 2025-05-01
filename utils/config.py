import os
from google import genai 
from google.genai import types
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from io import BytesIO
import base64

def configure_api():
    """Configure Google Generative AI and return a client"""
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key:
        return None
    
    # Create and return client instance directly (no configure method needed)
    return genai.Client(api_key=api_key)

# Available models
MODELS = {
    "default": "models/gemini-2.0-flash",
    "advanced": "models/gemini-2.5-flash-preview-04-17",
    "pro": "models/gemini-2.0-pro",
    "image_gen": "gemini-2.0-flash-exp-image-generation"  # New model for image generation
}

def generate_image(client, prompt):
    """Generate an image based on a text prompt using Gemini."""
    try:
        response = client.models.generate_content(
            model=MODELS["image_gen"],
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        # Process response for images
        image_data = None
        text_response = None
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text_response = part.text
            elif part.inline_data is not None:
                image_data = part.inline_data.data
                
        return text_response, image_data
    except Exception as e:
        return str(e), None

# Analogy styles available
ANALOGY_STYLES = {
    "Tech": "Use technology analogies (computers, networks, etc.)",
    "Nature": "Use nature-related analogies (ecosystems, animals, etc.)",
    "Cooking": "Use culinary analogies (recipes, ingredients, etc.)",
    "Sports": "Use sports analogies (game rules, strategies, etc.)",
    "Pop Culture": "Use popular culture references (movies, series, etc.)"
}

# Available fields of expertise
FIELDS = [
    "Computer Science", "Artificial Intelligence", "Web Development", 
    "Data Science", "Cybersecurity", "Medicine", "Biology", 
    "Physics", "Mathematics", "Psychology", "Economics", 
    "Law", "Philosophy", "Other"
]

# Knowledge levels
KNOWLEDGE_LEVELS = ["Novice", "Intermediate", "Expert"]
