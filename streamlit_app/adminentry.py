import streamlit as st
import requests
import datetime

API_URL = "http://localhost:8000"


def app():
    st.title("🛠️ Modifier ou Supprimer une Observation")

    token = st.session_state.get("token")
    if not token:
        st.error("Vous devez être connecté pour gérer le traitement des observations.")
        return

    st.markdown(
        """
    Récupérez l'ID de l'observation concernée dans l'onglet **Calendrier** (dans "Informations supplémentaires sous forme de liste").
    """
    )

    if "entry_id" not in st.session_state:
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

        # Auth headers
        headers = {"Authorization": f"Bearer {token}"}

        # Récupération de l'entrée
        try:
            entry_resp = requests.get(
                f"{API_URL}/entry/{entry_id}", headers=headers, timeout=60
            )
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
        try:
            triggers_list = [
                t["name"]
                for t in requests.get(
                    f"{API_URL}/triggers/", headers=headers, timeout=60
                ).json()
            ]
            reactions_list = [
                r["name"]
                for r in requests.get(
                    f"{API_URL}/reactions/", headers=headers, timeout=60
                ).json()
            ]
        except Exception as e:
            st.warning(
                f"Erreur lors de la récupération des déclencheurs ou réactions : {e}"
            )
            triggers_list = []
            reactions_list = []

        # Champs modifiables
        st.subheader("✏️ Modifier l'entrée")

        entry_date = st.date_input(
            "Date", value=datetime.date.fromisoformat(entry["entry_date"])
        )
        severity = st.slider("Gravité", 1, 5, entry["severity"])
        comment = st.text_area("Commentaire", value=entry.get("comment", ""))

        selected_trigger = st.selectbox(
            "Déclencheur",
            triggers_list,
            index=triggers_list.index(entry["triggers"][0]) if entry["triggers"] else 0,
        )
        selected_reaction = st.selectbox(
            "Réaction",
            reactions_list,
            index=(
                reactions_list.index(entry["reactions"][0]) if entry["reactions"] else 0
            ),
        )

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
                    update_resp = requests.put(
                        f"{API_URL}/entry/{entry_id}",
                        headers=headers,
                        timeout=60,
                        json=payload,
                    )
                    update_resp.raise_for_status()
                    st.success("✅ Entrée modifiée avec succès.")
                    st.session_state.entry_id = ""
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")

        with col2:
            if st.button("🗑️ Supprimer l'entrée"):
                try:
                    delete_resp = requests.delete(
                        f"{API_URL}/entry/{entry_id}", headers=headers, timeout=60
                    )
                    delete_resp.raise_for_status()
                    st.success("✅ Entrée supprimée.")
                    st.session_state.entry_id = ""
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")

        with col3:
            if st.button("🔙 Retour"):
                st.session_state.entry_id = ""
                st.rerun()
