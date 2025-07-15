import streamlit as st
import requests

API_URL = "http://localhost:8000"


def app():
    st.title("Réinitialisation du mot de passe")

    query_params = st.query_params
    token = query_params.get("token")

    if not token:
        st.error("Le token est manquant dans l'URL.")
        return

    new_password = st.text_input("Nouveau mot de passe", type="password")
    confirm_password = st.text_input("Confirmer le mot de passe", type="password")

    if st.button("Réinitialiser le mot de passe"):
        if not new_password or not confirm_password:
            st.warning("Merci de remplir tous les champs.")
        elif new_password != confirm_password:
            st.error("Les mots de passe ne correspondent pas.")
        else:
            response = requests.post(
                f"{API_URL}/password-reset/reset-password",
                json={"token": token, "new_password": new_password},
            )
            if response.status_code == 200:
                st.success(
                    "Mot de passe réinitialisé avec succès. Vous pouvez maintenant vous connecter."
                )
            else:
                try:
                    detail = response.json().get("detail", "Erreur inconnue.")
                except Exception:
                    detail = "Erreur inconnue."
                st.error(f"Erreur : {detail}")
