import streamlit as st

def app():
    st.markdown(
        """
        <h2 style='color: #4CAF50;'>🐾 Bienvenue sur Mon Suivi de Réactivité 🐾</h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.write("""
    **Mon Suivi de Réactivité** est une application simple et efficace pour :
    
    - **Ajouter des observations** sur les réactions de votre chien
    - **Analyser** son évolution dans le temps
    - **Visualiser** ses progrès sur un calendrier
    - **Rechercher** des déclencheurs spécifiques
    """)
    
    st.info("👉 Utilisez le menu de gauche pour naviguer dans l'application.")

    st.markdown("---")

    st.subheader("Statistiques rapides")
    st.write("- **Nombre d'entrées** : _(à venir)_")
    st.write("- **Dernière entrée** : _(à venir)_")