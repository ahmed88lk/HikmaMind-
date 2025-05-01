import streamlit as st
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserProfile:
    """Class representing a user profile"""
    field: str = "Computer Science"
    knowledge_level: str = "Intermediate"
    analogy_style: str = "Tech" 
    include_citations: bool = False
    
    def is_complete(self) -> bool:
        """Check if the profile is complete"""
        return bool(self.field and self.knowledge_level and self.analogy_style is not None)
    
    def get_prompt_modifier(self) -> str:
        """Return a string representing prompt modifications based on profile"""
        modifiers = []
        
        # Adaptations based on knowledge level
        if self.knowledge_level == "Novice":
            modifiers.append("Use very simple analogies and avoid technical jargon.")
            modifiers.append("Explain as to someone completely new to the subject.")
        elif self.knowledge_level == "Intermediate":
            modifiers.append("Use some technical terms but explain them.")
            modifiers.append("Connect with basic domain concepts.")
        elif self.knowledge_level == "Expert":
            modifiers.append("Technical jargon is acceptable without lengthy explanations.")
            modifiers.append("Reference advanced concepts in the field.")
        
        # Adaptations based on analogy style
        if self.analogy_style == "Tech":
            modifiers.append("Use analogies related to computers, networks and technologies.")
        elif self.analogy_style == "Nature":
            modifiers.append("Use analogies related to nature, animals and ecosystems.")
        elif self.analogy_style == "Cooking":
            modifiers.append("Use analogies related to cooking, recipes and ingredients.")
        elif self.analogy_style == "Sports":
             modifiers.append("Use analogies related to sports, games, training, and athletic performance.")
        elif self.analogy_style == "Pop Culture":
            modifiers.append("Use analogies related to movies, series, and popular culture references.")

def initialize_session_state():
    """Initialize session state variables if necessary"""
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = UserProfile()

def save_profile(profile: UserProfile):
    """Save user profile in session state"""
    st.session_state.user_profile = profile

def get_current_profile() -> UserProfile:
    """Get current user profile"""
    initialize_session_state()
    return st.session_state.user_profile



