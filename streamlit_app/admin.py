import streamlit as st
import requests

API_URL = "http://localhost:8000"

def app():
    st.title("Administration : Déclencheurs et Réactions")

    token = st.session_state.get("token")
    if not token:
        st.error("Vous devez être connecté pour gérer les déclencheurs et réactions.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # -------------------
    # DÉCLENCHEURS
    # -------------------
    st.subheader("Déclencheurs")

    try:
        triggers = requests.get(f"{API_URL}/triggers/", headers=headers).json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des déclencheurs : {e}")
        triggers = []

    for trigger in triggers:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_name = st.text_input(f"Modifier '{trigger['name']}'", value=trigger['name'], key=f"trigger_{trigger['id']}")
        with col2:
            if st.button("🗑️ Supprimer", key=f"delete_trigger_{trigger['id']}"):
                try:
                    requests.delete(f"{API_URL}/triggers/{trigger['id']}", headers=headers)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur lors de la suppression : {e}")
        if new_name != trigger['name']:
            try:
                requests.put(f"{API_URL}/triggers/{trigger['id']}", headers=headers, json={"name": new_name})
                st.rerun()
            except Exception as e:
                st.error(f"Erreur lors de la mise à jour : {e}")

    # Ajouter un déclencheur
    st.subheader("Ajouter un nouveau déclencheur")
    new_trigger_name = st.text_input("Nom du nouveau déclencheur", key="new_trigger_name")
    if st.button("Ajouter le déclencheur"):
        if new_trigger_name:
            try:
                requests.post(f"{API_URL}/triggers/", headers=headers, json={"name": new_trigger_name})
                st.rerun()
            except Exception as e:
                st.error(f"Erreur lors de l'ajout : {e}")
        else:
            st.warning("Veuillez entrer un nom pour le déclencheur.")

    # -------------------
    # RÉACTIONS
    # -------------------
    st.subheader("Réactions")

    try:
        reactions = requests.get(f"{API_URL}/reactions/", headers=headers).json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des réactions : {e}")
        reactions = []

    for reaction in reactions:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_name = st.text_input(f"Modifier '{reaction['name']}'", value=reaction['name'], key=f"reaction_{reaction['id']}")
        with col2:
            if st.button("🗑️ Supprimer", key=f"delete_reaction_{reaction['id']}"):
                try:
                    requests.delete(f"{API_URL}/reactions/{reaction['id']}", headers=headers)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur lors de la suppression : {e}")
        if new_name != reaction['name']:
            try:
                requests.put(f"{API_URL}/reactions/{reaction['id']}", headers=headers, json={"name": new_name})
                st.rerun()
            except Exception as e:
                st.error(f"Erreur lors de la mise à jour : {e}")

    # Ajouter une réaction
    st.subheader("Ajouter une nouvelle réaction")
    new_reaction_name = st.text_input("Nom de la nouvelle réaction", key="new_reaction_name")
    if st.button("Ajouter la réaction"):
        if new_reaction_name:
            try:
                requests.post(f"{API_URL}/reactions/", headers=headers, json={"name": new_reaction_name})
                st.rerun()
            except Exception as e:
                st.error(f"Erreur lors de l'ajout : {e}")
        else:
            st.warning("Veuillez entrer un nom pour la réaction.")
