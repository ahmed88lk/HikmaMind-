import streamlit as st
from utils.config import ANALOGY_STYLES, FIELDS, KNOWLEDGE_LEVELS
from models.user_profile import UserProfile, save_profile, get_current_profile

def render_header():
    """Affiche l'en-tête de l'application"""
    st.title("🧠 HikmaMind")
    st.subheader("Transformez des concepts complexes en analogies personnalisées")
    
    st.markdown("""
    Cette application utilise l'IA pour aider les chercheurs et professionnels à comprendre 
    des articles de recherche ou des vidéos YouTube en créant des analogies adaptées 
    à votre niveau de connaissance et votre style d'apprentissage préféré.
    """)

def render_about():
    """Affiche la section À propos"""
    st.markdown("---")
    st.markdown("""
    ### À propos de HikmaMind

    HikmaMind est conçu pour aider les professionnels de l'informatique et de la recherche à comprendre rapidement 
    des concepts complexes grâce à des analogies et des résumés générés par l'IA et personnalisés selon votre profil.

    **Technologies utilisées:**
    - Streamlit pour l'interface utilisateur
    - Google Gemini AI pour l'analyse de contenu
    - Support pour les vidéos YouTube et documents PDF
    
    **Comment ça marche:**
    1. Complétez votre profil d'apprentissage
    2. Soumettez une vidéo ou un document
    3. Obtenez des explications adaptées à votre niveau et style
    """)

def render_sidebar():
    """Affiche et gère le profil utilisateur dans la barre latérale"""
    st.sidebar.title("Votre profil d'apprentissage")
    
    # Récupérer le profil actuel
    current_profile = get_current_profile()
    
    # Formulaire pour mettre à jour le profil
    with st.sidebar.form("user_profile_form"):
        st.subheader("Personnalisez vos explications")
        
        field = st.selectbox(
            "Votre domaine d'expertise",
            options=FIELDS,
            index=FIELDS.index(current_profile.field) if current_profile.field in FIELDS else 0
        )
        
        knowledge_level = st.radio(
            "Votre niveau de connaissance",
            options=KNOWLEDGE_LEVELS,
            index=KNOWLEDGE_LEVELS.index(current_profile.knowledge_level) if current_profile.knowledge_level in KNOWLEDGE_LEVELS else 0,
            help="Cela nous aide à adapter le niveau de détail et de jargon"
        )
        
        analogy_style = st.selectbox(
            "Style d'analogies préféré",
            options=list(ANALOGY_STYLES.keys()),
            index=list(ANALOGY_STYLES.keys()).index(current_profile.analogy_style) if current_profile.analogy_style in ANALOGY_STYLES else 0,
            help="Choisissez le type d'analogies qui vous parle le plus"
        )
        
        include_citations = st.checkbox(
            "Inclure des citations/références",
            value=current_profile.include_citations,
            help="Ajouter des références aux sources originales"
        )
        
        submitted = st.form_submit_button("Enregistrer mon profil")
        
        if submitted:
            # Mettre à jour le profil
            updated_profile = UserProfile(
                field=field,
                knowledge_level=knowledge_level,
                analogy_style=analogy_style,
                include_citations=include_citations
            )
            save_profile(updated_profile)
            st.sidebar.success("✅ Profil enregistré avec succès!")
            return updated_profile
    
    # Afficher un résumé du profil actuel
    if current_profile.is_complete():
        st.sidebar.markdown("---")
        st.sidebar.subheader("Résumé de votre profil")
        st.sidebar.markdown(f"""
        - **Domaine:** {current_profile.field}
        - **Niveau:** {current_profile.knowledge_level}
        - **Style d'analogies:** {current_profile.analogy_style}
        - **Citations:** {"Oui" if current_profile.include_citations else "Non"}
        """)
    
    return current_profile
