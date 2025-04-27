import streamlit as st
import requests

st.title("Mon Suivi de Réactivité")

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

# Dictionnaire pour la navigation
PAGES = {
    "Accueil": Home,
    "Nouvelle entrée": dataentry,
    "Analyses": analysis,
    "Calendrier": calender,
    "Recherches": research
}

# Sidebar pour choisir la page
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Aller vers :", list(PAGES.keys()))

# Afficher la page sélectionnée
page = PAGES[selection]
page.app()
