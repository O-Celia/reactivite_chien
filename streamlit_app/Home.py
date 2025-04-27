import streamlit as st

def app():
    st.title("🐾 Bienvenue sur le suivi de réactivité de ton chien 🐾")
    
    st.write("""
    Cette application vous permet de :
    - Enregistrer les réactions de votre chien face à différents déclencheurs
    - Suivre l'évolution dans le temps
    - Visualiser les progrès sous forme de graphiques et de calendrier
    - Rechercher des déclencheurs spécifiques
    """)

    st.info("👉 Pour commencer, allez dans 'Nouvelle entrée' via le menu de gauche.")

    st.markdown("---")
    st.subheader("Statistiques rapides (bientôt disponibles) :")
    st.write("- Nombre total d'entrées : (à venir)")
    st.write("- Dernière entrée : (à venir)")