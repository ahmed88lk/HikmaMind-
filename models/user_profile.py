import streamlit as st
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserProfile:
    """Classe représentant le profil d'un utilisateur"""
    field: str = "Informatique"
    knowledge_level: str = "Intermédiaire"
    analogy_style: str = "Tech" 
    include_citations: bool = False
    
    def is_complete(self) -> bool:
        """Vérifie si le profil est complet"""
        return bool(self.field and self.knowledge_level and self.analogy_style is not None)
    
    def get_prompt_modifier(self) -> str:
        """Retourne une chaîne représentant les modifications de prompt basées sur le profil"""
        modifiers = []
        
        # Adaptations selon le niveau de connaissance
        if self.knowledge_level == "Novice":
            modifiers.append("Utilisez des analogies très simples et évitez tout jargon technique.")
            modifiers.append("Expliquez comme à quelqu'un qui découvre le sujet.")
        elif self.knowledge_level == "Intermédiaire":
            modifiers.append("Utilisez quelques termes techniques mais expliquez-les.")
            modifiers.append("Établissez des liens avec des concepts de base du domaine.")
        elif self.knowledge_level == "Expert":
            modifiers.append("Vous pouvez utiliser du jargon technique sans longues explications.")
            modifiers.append("Faites référence à des concepts avancés dans le domaine.")
        
        # Adaptations selon le style d'analogie
        if self.analogy_style == "Tech":
            modifiers.append("Utilisez des analogies liées aux ordinateurs, réseaux et technologies.")
        elif self.analogy_style == "Nature":
            modifiers.append("Utilisez des analogies liées à la nature, aux animaux et aux écosystèmes.")
        elif self.analogy_style == "Cuisine":
            modifiers.append("Utilisez des analogies liées à la cuisine, aux recettes et aux ingrédients.")
        elif self.analogy_style == "Sport":
            modifiers.append("Utilisez des analogies liées aux sports, aux règles du jeu et aux stratégies.")
        elif self.analogy_style == "Pop Culture":
            modifiers.append("Utilisez des références à des films, séries, jeux vidéo populaires.")
            
        return "\n".join(modifiers)

def initialize_session_state():
    """Initialise les variables d'état de session si nécessaires"""
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = UserProfile()

def save_profile(profile: UserProfile):
    """Enregistre le profil utilisateur dans l'état de la session"""
    st.session_state.user_profile = profile

def get_current_profile() -> UserProfile:
    """Récupère le profil utilisateur actuel"""
    initialize_session_state()
    return st.session_state.user_profile
