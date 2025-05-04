import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/entry"

def app():
    
    token = st.session_state.get("token", None)
    if not token:
        st.warning("Vous devez être connecté pour voir cette page.")
        st.stop()
    headers = {"Authorization": f"Bearer {token}"}

    st.markdown(
        """
        <h2 style='color: #4CAF50;'>🐾 Bienvenue sur votre suivi de réactivité 🐾</h2>
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
    
    # 1. Nombre d'entrées
    response_count = requests.get(f"{API_URL}/", headers=headers)
    if response_count.status_code == 200:
        entries = response_count.json()
        nb_entries = len(entries)
    else:
        nb_entries = 0

    # 2. Dernière entrée

    response_last = requests.get(f"{API_URL}/", headers=headers)
    if response_last.status_code == 200:
        entries = response_last.json()
        if entries:
            df_entries = pd.DataFrame(entries)
            if "entry_date" in df_entries.columns:
                df_entries["entry_date"] = pd.to_datetime(df_entries["entry_date"])
                last_entry = df_entries["entry_date"].max().strftime("%d/%m/%Y")
            else:
                last_entry = "Date manquante dans les données"
        else:
            last_entry = "Aucune entrée"
    else:
        last_entry = "Erreur de récupération"

    st.subheader("Statistiques rapides")
    st.write(f"- **Nombre d'entrées** : {nb_entries}")
    st.write(f"- **Dernière entrée** : {last_entry}")