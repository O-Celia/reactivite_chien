import streamlit as st
import requests

# username = st.text_input("Nom d'utilisateur")
# password = st.text_input("Mot de passe", type="password")

# if st.button("Connexion"):
#     response = requests.post("http://localhost:8000/users/login", json={"username": username, "password": password})
#     if response.status_code == 200:
#         st.success("Connecté !")
#     else:
#         st.error("Nom d'utilisateur ou mot de passe incorrect")

# Importation des différentes pages
import Home
import dataentry
import analysis
import calender
import research
import adminentry
import admin

# Dictionnaire pour la navigation
PAGES = {
    "Accueil": Home,
    "Nouvelle entrée": dataentry,
    "Calendrier": calender,
    "Recherches": research,
    "Analyses graphiques": analysis,
    "Gestion des entrées" : adminentry,
    "Administration" : admin
}

def app():
    st.sidebar.title("Navigation")

    selection = st.sidebar.selectbox("Aller vers :", list(PAGES.keys()))

    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    app()