import streamlit as st
import requests
import datetime

API_URL = "http://localhost:8000"

def app():
    st.title("Nouvelle observation")

    # Valeurs par défaut
    defaults = {
        "username": "",
        "entry_date": datetime.date.today(),
        "severity": 3,
        "comment": "",
        "existing_trigger": "",
        "new_trigger": "",
        "existing_reaction": "",
        "new_reaction": "",
        "reset_triggered": False,  # Flag pour réinitialiser
    }

    # Initialisation des clés en session_state, sauf si déjà instanciées par un widget
    for key, default in defaults.items():
        st.session_state.setdefault(key, default)

    # Si le flag de réinitialisation est activé, réinitialiser session_state
    if st.session_state.get("reset_triggered"):
        for key, default in defaults.items():
            if key != "reset_triggered":  # Ne pas réinitialiser le flag
                st.session_state[key] = default
        st.session_state["reset_triggered"] = False  # Réinitialiser le flag

    # Interface utilisateur
    st.text_input("Nom d'utilisateur", key="username")
    st.date_input("Date de l'observation", key="entry_date")
    st.slider("Niveau de gravité (1 = léger, 5 = intense)", 1, 5, key="severity")
    st.text_area("Commentaire", key="comment")

    # Récupération des options
    try:
        triggers = requests.get(f"{API_URL}/triggers/").json()
        reactions = requests.get(f"{API_URL}/reactions/").json()
    except:
        triggers = []
        reactions = []

    trigger_names = [""] + [t["name"] for t in triggers]
    reaction_names = [""] + [r["name"] for r in reactions]

    st.selectbox("Déclencheur existant :", trigger_names, key="existing_trigger")
    st.text_input("...ou ajouter un nouveau déclencheur", key="new_trigger")

    st.selectbox("Réaction existante :", reaction_names, key="existing_reaction")
    st.text_input("...ou ajouter une nouvelle réaction", key="new_reaction")

    # Boutons en bas : deux colonnes
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Soumettre l'observation"):
            try:
                user_resp = requests.get(f"{API_URL}/users/{st.session_state.username}")
                user_id = user_resp.json().get("id")
            except:
                st.error("Utilisateur non trouvé.")
                return

            trigger = st.session_state.new_trigger.strip() or st.session_state.existing_trigger
            reaction = st.session_state.new_reaction.strip() or st.session_state.existing_reaction

            if not trigger or not reaction:
                st.warning("Merci de renseigner au moins un déclencheur ET une réaction.")
                return

            payload = {
                "user_id": user_id,
                "entry_date": str(st.session_state.entry_date),
                "severity": st.session_state.severity,
                "comment": st.session_state.comment,
                "triggers": [trigger],
                "reactions": [reaction],
            }

            resp = requests.post(f"{API_URL}/entry/", json=payload)
            if resp.status_code in [200, 201]:
                st.success("Observation enregistrée avec succès.")
            else:
                st.error(f"Erreur lors de l'enregistrement : {resp.text}")

    with col2:
        if st.button("Réinitialiser"):
            st.session_state["reset_triggered"] = True
            st.rerun()
