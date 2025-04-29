import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000/entry"

def app():
    st.title("Supprimer une entrée")

    st.markdown("""
    Pour supprimer une entrée, récupérez son ID dans l'onglet **Calendrier** (dans "Informations supplémentaires sous forme de liste").
    """)

    if 'entry_id' not in st.session_state:
        st.session_state.entry_id = ""  # Initialiser l'ID si ce n’est pas déjà fait

    # Demande de l'ID de l'entrée
    if st.session_state.entry_id == "":
        entry_id = st.text_input("ID de l'entrée à supprimer :", key="entry_id_input")

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
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                st.error(f"Erreur 404 : entrée avec ID {entry_id} non trouvée.")
                if st.button("Réessayer"):
                    st.session_state.entry_id = ""  # Réinitialiser l'ID
                    st.rerun()
                return
            else:
                st.error(f"Erreur HTTP : {http_err}")
                return
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion : {e}")
            return

        st.markdown("---")
        st.subheader("Données de l'entrée sélectionnée")

        st.write(f"📅 **Date** : {entry_data.get('entry_date', 'N/A')}")
        st.write(f"💬 **Commentaire** : {entry_data.get('comment', 'Aucun')}")

        triggers = ", ".join(entry_data.get("triggers", [])) or "Aucun"
        reactions = ", ".join(entry_data.get("reactions", [])) or "Aucune"
        severity = entry_data.get("severity", "Non précisé")

        st.write(f"⚡ **Déclencheur(s)** : {triggers}")
        st.write(f"😮 **Réaction(s)** : {reactions}")
        st.write(f"🔥 **Intensité** : {severity} / 5")
        
        st.markdown("<br> <br>", unsafe_allow_html=True)

        st.markdown("⚠️ **Attention : Cette action est irréversible.**")

        if st.button("Supprimer l'entrée", type="primary"):
            try:
                response = requests.delete(f"{API_URL}/{entry_id}")
                if response.status_code == 200:
                    st.success("Entrée supprimée avec succès !")
                    st.session_state.entry_id = ""
                    st.rerun()
                else:
                    st.error(f"Erreur {response.status_code} : {response.text}")
            except requests.exceptions.RequestException as e:
                    st.error(f"Erreur lors de la récupération de l'entrée : {e}")
