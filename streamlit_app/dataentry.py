import streamlit as st
import requests
import datetime

API_URL = "http://localhost:8000"

def app():
    st.title("Nouvelle observation")

    # Saisie de l'utilisateur (temporaire, remplacé plus tard par l'auth)
    username = st.text_input("Nom d'utilisateur")

    # Date de l'observation
    entry_date = st.date_input("Date de l'observation", value=datetime.date.today())

    severity = st.slider("Niveau de gravité (1 = léger, 5 = intense)", 1, 5, 3)
    comment = st.text_area("Commentaire")

    # Récupération des déclencheurs et réactions existants via API
    try:
        triggers_resp = requests.get(f"{API_URL}/triggers/")
        reactions_resp = requests.get(f"{API_URL}/reactions/")
        triggers = triggers_resp.json() if triggers_resp.status_code == 200 else []
        reactions = reactions_resp.json() if reactions_resp.status_code == 200 else []
        triggers_list = [t['name'] for t in triggers]
        reactions_list = [r['name'] for r in reactions]
    except:
        st.error("Erreur de récupération des déclencheurs/réactions.")
        triggers_list = []
        reactions_list = []

    st.subheader("Déclencheurs")
    existing_trigger = st.selectbox("Déclencheur existant :", [""] + triggers_list)
    new_trigger = st.text_input("...ou ajouter un nouveau déclencheur")

    st.subheader("Réactions observées")
    existing_reaction = st.selectbox("Réaction existante :", [""] + reactions_list)
    new_reaction = st.text_input("...ou ajouter une nouvelle réaction")

    if st.button("Soumettre l'observation"):
        # Identification de l'utilisateur
        user_resp = requests.get(f"{API_URL}/users/{username}")
        if user_resp.status_code != 200:
            st.error("Utilisateur non trouvé.")
            return
        user_id = user_resp.json().get("id")

        # Détermination du déclencheur
        trigger_final = new_trigger.strip() if new_trigger.strip() else existing_trigger
        reaction_final = new_reaction.strip() if new_reaction.strip() else existing_reaction

        # Vérification
        if not trigger_final or not reaction_final:
            st.warning("Merci de renseigner au moins un déclencheur ET une réaction.")
            return

        # Construction du payload
        payload = {
            "user_id": user_id,
            "entry_date": str(entry_date),
            "severity": severity,
            "comment": comment,
            "triggers": [trigger_final],
            "reactions": [reaction_final]
        }

        response = requests.post(f"{API_URL}/entry/", json=payload)

        if response.status_code in [200, 201]:
            st.success("Observation enregistrée avec succès.")
        else:
            st.error(f"Erreur lors de l'enregistrement : {response.text}")

