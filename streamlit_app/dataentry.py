import streamlit as st
import requests
import datetime

API_URL = "http://localhost:8000"


def app():
    st.title("Nouvelle observation")

    # Valeurs par défaut
    defaults = {
        "entry_date": datetime.date.today(),
        "severity": 3,
        "comment": "",
        "existing_trigger": "",
        "new_trigger": "",
        "existing_reaction": "",
        "new_reaction": "",
        "reset_triggered": False,
    }

    # Initialisation session_state
    for key, default in defaults.items():
        st.session_state.setdefault(key, default)

    if st.session_state.get("reset_triggered"):
        for key, default in defaults.items():
            if key != "reset_triggered":
                st.session_state[key] = default
        st.session_state["reset_triggered"] = False

    # Authentification
    token = st.session_state.get("token")
    if not token:
        st.error("Vous devez être connecté pour enregistrer une observation.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # Interface utilisateur
    st.date_input("Date de l'observation", key="entry_date")
    st.slider("Niveau de gravité (1 = léger, 5 = intense)", 1, 5, key="severity")
    st.text_area("Commentaire", key="comment")

    # Récupération déclencheurs / réactions
    try:
        triggers = requests.get(
            f"{API_URL}/triggers/", headers=headers, timeout=60
        ).json()
        reactions = requests.get(
            f"{API_URL}/reactions/", headers=headers, timeout=60
        ).json()
    except Exception as e:
        st.error(f"Erreur de chargement des déclencheurs ou réactions : {e}")
        triggers, reactions = [], []

    trigger_names = [""] + [t["name"] for t in triggers]
    reaction_names = [""] + [r["name"] for r in reactions]

    st.selectbox("Déclencheur existant :", trigger_names, key="existing_trigger")
    st.text_input("...ou ajouter un nouveau déclencheur", key="new_trigger")

    st.selectbox("Réaction existante :", reaction_names, key="existing_reaction")
    st.text_input("...ou ajouter une nouvelle réaction", key="new_reaction")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Soumettre l'observation"):

            # Choix final du déclencheur et de la réaction
            trigger = (
                st.session_state.new_trigger.strip()
                or st.session_state.existing_trigger
            )
            reaction = (
                st.session_state.new_reaction.strip()
                or st.session_state.existing_reaction
            )

            # Création si déclencheur nouveau
            if trigger and trigger not in trigger_names:
                trigger_payload = {"name": trigger}
                trigger_resp = requests.post(
                    f"{API_URL}/triggers/",
                    json=trigger_payload,
                    headers=headers,
                    timeout=60,
                )
                if trigger_resp.status_code not in [200, 201]:
                    st.error(
                        f"Erreur lors de l'ajout du déclencheur : {trigger_resp.text}"
                    )
                    return

            # Création si réaction nouvelle
            if reaction and reaction not in reaction_names:
                reaction_payload = {"name": reaction}
                reaction_resp = requests.post(
                    f"{API_URL}/reactions/",
                    json=reaction_payload,
                    headers=headers,
                    timeout=60,
                )
                if reaction_resp.status_code not in [200, 201]:
                    st.error(
                        f"Erreur lors de l'ajout de la réaction : {reaction_resp.text}"
                    )
                    return

            # Création de l'observation
            payload = {
                "entry_date": str(st.session_state.entry_date),
                "severity": st.session_state.severity,
                "comment": st.session_state.comment,
                "triggers": [trigger] if trigger else [],
                "reactions": [reaction] if reaction else [],
            }

            resp = requests.post(
                f"{API_URL}/entry/", json=payload, headers=headers, timeout=60
            )
            if resp.status_code in [200, 201]:
                st.success("Observation enregistrée avec succès.")
            else:
                st.error(f"Erreur lors de l'enregistrement : {resp.text}")

    with col2:
        if st.button("Réinitialiser"):
            st.session_state["reset_triggered"] = True
            st.rerun()
