import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000/entry"

def app():
    st.title("Modifier les données")

    st.markdown("""
    Pour modifier une entrée, récupérez son ID dans l'onglet **Calendrier** (dans "Informations supplémentaires sous forme de liste").
    """)

    if 'entry_id' not in st.session_state:
        st.session_state.entry_id = ""  # Initialiser l'ID si ce n'est pas déjà fait

    # Demande de l'ID de l'entrée
    if st.session_state.entry_id == "":
        entry_id = st.text_input("ID de l'entrée à modifier :", key="entry_id_input")

        if st.button("Confirmer l'ID"):
            if not entry_id:
                st.warning("Veuillez entrer un ID.")
            else:
                st.session_state.entry_id = entry_id
                st.rerun()

    else:  # Si l'ID a été confirmé et est stocké
        entry_id = st.session_state.entry_id

        # Récupération de l'entrée existante
        try:
            response = requests.get(f"{API_URL}/{entry_id}")
            response.raise_for_status()
            entry_data = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de la récupération de l'entrée : {e}")
            return

        st.markdown("---")

        # Champs pour modification
        new_date = st.date_input("Date", value=datetime.strptime(entry_data.get("entry_date"), "%Y-%m-%d").date())
        new_comment = st.text_area("Commentaire", value=entry_data.get("comment", ""))
        
        # Récupération dynamique des déclencheurs et réactions depuis l'API
        try:
            triggers_resp = requests.get("http://localhost:8000/triggers/")
            reactions_resp = requests.get("http://localhost:8000/reactions/")
            triggers = triggers_resp.json() if triggers_resp.status_code == 200 else []
            reactions = reactions_resp.json() if reactions_resp.status_code == 200 else []
            triggers_list = [t['name'] for t in triggers]
            reactions_list = [r['name'] for r in reactions]
        except:
            st.error("Erreur de récupération des déclencheurs/réactions.")
            triggers_list = []
            reactions_list = []

        # Filtrage des valeurs par défaut pour éviter les erreurs Streamlit
        default_triggers = [t for t in entry_data.get("triggers", []) if t in triggers_list]
        default_reactions = [r for r in entry_data.get("reactions", []) if r in reactions_list]

        new_trigger = st.selectbox("Déclencheur", triggers_list, index=triggers_list.index(default_triggers[0]) if default_triggers else 0)
        new_reaction = st.selectbox("Réaction", reactions_list, index=reactions_list.index(default_reactions[0]) if default_reactions else 0)

        new_severity = st.slider("Intensité (1 = faible, 5 = forte)", 1, 5, value=entry_data.get("severity", 1))

        if st.button("Mettre à jour l'entrée"):
            updated_entry = {
                "user": new_user,
                "entry_date": new_date.isoformat(),
                "comment": new_comment,
                "triggers": [new_trigger],
                "reactions": [new_reaction],
                "severity": new_severity,
            }

            try:
                response = requests.put(f"{API_URL}/{entry_id}", json=updated_entry)
                if response.status_code == 200:
                    st.success("Entrée mise à jour avec succès !")
                    st.session_state.entry_id = ""
                    st.rerun() 
                else:
                    st.error(f"Erreur {response.status_code} : {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors de la mise à jour : {e}")
