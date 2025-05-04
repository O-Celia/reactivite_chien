import streamlit as st
import requests

API_URL = "http://localhost:8000"

def app():
    st.title("Administration : Déclencheurs et Réactions")

    token = st.session_state.get("token")
    if not token:
        st.error("Vous devez être connecté pour gérer le traitement des déclencheurs et réactions.")
        return

    # Déclencheurs
    st.subheader("Déclencheurs")
    
    # Afficher les déclencheurs existants
    headers = {"Authorization": f"Bearer {token}"}
    user_resp = requests.get(f"{API_URL}/users/me", headers=headers)
    user_id = user_resp.json().get("id")
    triggers = requests.get(f"{API_URL}/triggers/", params={"user_id": user_id}, headers=headers).json()
    for trigger in triggers:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_name = st.text_input(f"Modifier '{trigger['name']}'", value=trigger['name'], key=f"trigger_{trigger['id']}")
        with col2:
            if st.button("🗑️ Supprimer", key=f"delete_trigger_{trigger['id']}"):
                requests.delete(f"{API_URL}/triggers/{trigger['id']}", headers=headers)
                st.rerun()
        if new_name != trigger['name']:
            requests.put(f"{API_URL}/triggers/{trigger['id']}", headers=headers, json={"name": new_name})
            st.rerun()

    # Ajouter un nouveau déclencheur
    st.subheader("Ajouter un nouveau déclencheur")
    new_trigger_name = st.text_input("Nom du nouveau déclencheur", key="new_trigger_name")
    if st.button("Ajouter le déclencheur"):
        if new_trigger_name:
            requests.post(f"{API_URL}/triggers/", headers=headers, json={"name": new_trigger_name, "user_id": user_id})
            st.rerun()
        else:
            st.warning("Veuillez entrer un nom pour le déclencheur.")

    # Réactions
    st.subheader("Réactions")
    
    # Afficher les réactions existantes
    reactions = requests.get(f"{API_URL}/reactions/", params={"user_id": user_id}, headers=headers).json()
    for reaction in reactions:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_name = st.text_input(f"Modifier '{reaction['name']}'", value=reaction['name'], key=f"reaction_{reaction['id']}")
        with col2:
            if st.button("🗑️ Supprimer", key=f"delete_reaction_{reaction['id']}"):
                requests.delete(f"{API_URL}/reactions/{reaction['id']}", headers=headers)
                st.rerun()
        if new_name != reaction['name']:
            requests.put(f"{API_URL}/reactions/{reaction['id']}", headers=headers, json={"name": new_name})
            st.rerun()

    # Ajouter une nouvelle réaction
    st.subheader("Ajouter une nouvelle réaction")
    new_reaction_name = st.text_input("Nom de la nouvelle réaction", key="new_reaction_name")
    if st.button("Ajouter la réaction"):
        if new_reaction_name:
            requests.post(f"{API_URL}/reactions/", headers=headers, json={"name": new_reaction_name, "user_id": user_id})
            st.rerun()
        else:
            st.warning("Veuillez entrer un nom pour la réaction.")

