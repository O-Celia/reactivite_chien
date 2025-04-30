import streamlit as st
import requests

API_URL = "http://localhost:8000"

def app():
    st.title("Administration : Déclencheurs et Réactions")

    st.subheader("Déclencheurs")
    triggers = requests.get(f"{API_URL}/triggers/").json()
    for trigger in triggers:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_name = st.text_input(f"Modifier '{trigger['name']}'", value=trigger['name'], key=f"trigger_{trigger['id']}")
        with col2:
            if st.button("🗑️ Supprimer", key=f"delete_trigger_{trigger['id']}"):
                requests.delete(f"{API_URL}/triggers/{trigger['id']}")
                st.rerun()
        if new_name != trigger['name']:
            requests.put(f"{API_URL}/triggers/{trigger['id']}", json={"name": new_name})
            st.rerun()

    st.subheader("Réactions")
    reactions = requests.get(f"{API_URL}/reactions/").json()
    for reaction in reactions:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_name = st.text_input(f"Modifier '{reaction['name']}'", value=reaction['name'], key=f"reaction_{reaction['id']}")
        with col2:
            if st.button("🗑️ Supprimer", key=f"delete_reaction_{reaction['id']}"):
                requests.delete(f"{API_URL}/reactions/{reaction['id']}")
                st.rerun()
        if new_name != reaction['name']:
            requests.put(f"{API_URL}/reactions/{reaction['id']}", json={"name": new_name})
            st.rerun()
