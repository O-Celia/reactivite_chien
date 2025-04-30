import streamlit as st
import requests
import datetime

API_URL = "http://localhost:8000"

def app():
    st.title("🛠️ Modifier ou Supprimer une Observation")

    st.markdown("""
    Récupérez l'ID de l'observation concernée dans l'onglet **Calendrier** (dans "Informations supplémentaires sous forme de liste").
    """)

    if 'entry_id' not in st.session_state:
        st.session_state.entry_id = ""

    if st.session_state.entry_id == "":
        entry_id = st.text_input("ID de l'entrée à gérer :", key="entry_id_input")

        if st.button("Charger l'entrée"):
            if not entry_id:
                st.warning("Veuillez entrer un ID.")
            else:
                st.session_state.entry_id = entry_id
                st.rerun()

    else:
        entry_id = st.session_state.entry_id

        # Récupération de l'entrée
        try:
            entry_resp = requests.get(f"{API_URL}/entry/{entry_id}")
            entry_resp.raise_for_status()
            entry = entry_resp.json()
        except requests.exceptions.HTTPError:
            st.error("Entrée non trouvée.")
            if st.button("Réessayer"):
                st.session_state.entry_id = ""
                st.rerun()
            return
        except Exception as e:
            st.error(f"Erreur : {e}")
            return

        # Récupération listes déclencheurs/réactions
        triggers_list = []
        reactions_list = []
        try:
            triggers_list = [t['name'] for t in requests.get(f"{API_URL}/triggers/").json()]
            reactions_list = [r['name'] for r in requests.get(f"{API_URL}/reactions/").json()]
        except:
            st.warning("Erreur lors de la récupération des déclencheurs ou réactions.")

        # Champs modifiables
        st.subheader("✏️ Modifier l'entrée")

        entry_date = st.date_input("Date", value=datetime.date.fromisoformat(entry["entry_date"]))
        severity = st.slider("Gravité", 1, 5, entry["severity"])
        comment = st.text_area("Commentaire", value=entry.get("comment", ""))

        selected_trigger = st.selectbox("Déclencheur", triggers_list, index=triggers_list.index(entry["triggers"][0]) if entry["triggers"] else 0)
        selected_reaction = st.selectbox("Réaction", reactions_list, index=reactions_list.index(entry["reactions"][0]) if entry["reactions"] else 0)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💾 Modifier"):
                payload = {
                    "entry_date": str(entry_date),
                    "severity": severity,
                    "comment": comment,
                    "triggers": [selected_trigger],
                    "reactions": [selected_reaction],
                }
                try:
                    update_resp = requests.put(f"{API_URL}/entry/{entry_id}", json=payload)
                    if update_resp.status_code == 200:
                        st.success("✅ Entrée modifiée avec succès.")
                        st.session_state.entry_id = ""
                        st.rerun()
                    else:
                        st.error(f"Erreur {update_resp.status_code} : {update_resp.text}")
                except Exception as e:
                    st.error(f"Erreur : {e}")

        with col2:
            if st.button("🗑️ Supprimer l'entrée"):
                delete_resp = requests.delete(f"{API_URL}/entry/{entry_id}")
                if delete_resp.status_code == 200:
                    st.success("✅ Entrée supprimée.")
                    st.session_state.entry_id = ""
                    st.rerun()
                else:
                    st.error(f"Erreur : {delete_resp.status_code} - {delete_resp.text}")
                    
        with col3:
            if st.button("🔙 Retour"):
                st.session_state.entry_id = ""
                st.rerun()
