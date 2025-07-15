import streamlit as st
import requests

API_URL = "http://localhost:8000"


def app():
    st.title("Mot de passe oublié")

    email = st.text_input("Adresse email", placeholder="Entrez votre adresse email")

    if st.button("Envoyer le lien de réinitialisation"):
        if email:
            response = requests.post(
                f"{API_URL}/password-reset/request-password-reset",
                json={"email": email},
            )
            if response.status_code == 200:
                st.success("Un email de réinitialisation a été envoyé.")
            else:
                st.error("Impossible d'envoyer l'email. Vérifiez l'adresse.")
        else:
            st.warning("Veuillez entrer votre adresse email.")
