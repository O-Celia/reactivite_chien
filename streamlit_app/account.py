# account.py
import streamlit as st
import requests

API_URL = "http://localhost:8000"


def app():
    st.title("Mon compte")

    token = st.session_state.get("token")
    if not token:
        st.warning("Vous devez être connecté pour voir cette page.")
        st.stop()

    headers = {"Authorization": f"Bearer {token}"}

    # Récupération des infos utilisateur
    response = requests.get(f"{API_URL}/users/me", headers=headers, timeout=60)

    if response.status_code == 200:
        user_data = response.json()
    else:
        st.error("Impossible de récupérer les données utilisateur.")
        return

    # Affichage et modification
    st.subheader("Modifier mes informations")
    new_username = st.text_input(
        "Nouveau nom d'utilisateur", value=user_data["username"]
    )
    new_email = st.text_input("Nouvel email", value=user_data["email"] or "")
    new_password = st.text_input("Nouveau mot de passe", type="password")

    if st.button("Mettre à jour mes infos"):
        payload = {}
        if new_username:
            payload["username"] = new_username
        if new_email:
            payload["email"] = new_email
        if new_password:
            payload["password"] = new_password

        update = requests.put(
            f"{API_URL}/users/me", json=payload, headers=headers, timeout=60
        )

        if update.status_code == 200:
            st.success("Informations mises à jour.")
            st.session_state["username"] = new_username
            st.rerun()
        else:
            st.error(update.json().get("detail", "Erreur inconnue."))

    st.subheader("Supprimer mon compte")
    confirm = st.checkbox("Je confirme la suppression de mon compte")
    if confirm:
        if st.button("🗑️ Supprimer mon compte"):
            delete = requests.delete(f"{API_URL}/users/me", headers=headers, timeout=60)
            if delete.status_code == 200:
                st.success("Compte supprimé.")
                st.session_state.clear()
                st.rerun()
            else:
                st.error(
                    delete.json().get(
                        "detail", "Erreur inconnue lors de la suppression."
                    )
                )
