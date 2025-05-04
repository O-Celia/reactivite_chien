import streamlit as st
import requests
import datetime
import pandas as pd

API_URL = "http://localhost:8000"

def app():
    st.title("Recherche d'observations")
    
    token = st.session_state.get("token")
    if not token:
        st.error("Vous devez être connecté pour faire des recherches.")
        return

    if "user_id" not in st.session_state:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            user_resp = requests.get(f"{API_URL}/users/me", headers=headers)
            user_resp.raise_for_status()
            user_id = user_resp.json().get("id")
            st.session_state["user_id"] = user_id
        except Exception as e:
            st.error(f"Impossible de récupérer les informations de l'utilisateur : {e}")
            return

    user_id = st.session_state["user_id"]

    # Valeurs par défaut
    defaults = {
        "query_text": "",
        "start_date": datetime.date.today() - datetime.timedelta(days=30),
        "end_date": datetime.date.today(),
        "selected_triggers": [],
        "selected_reactions": [],
        "selected_severities": [],
        "reset_triggered": False
    }

    # Initialisation de session_state
    for key, default in defaults.items():
        st.session_state.setdefault(key, default)

    # Réinitialisation
    if st.session_state.reset_triggered:
        for key, default in defaults.items():
            if key != "reset_triggered":
                st.session_state[key] = default
        st.session_state.reset_triggered = False
        st.rerun()

    # Champs de recherche
    st.text_input("Recherche (commentaire, contenu libre)", key="query_text")

    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Date de début", key="start_date")
    with col2:
        st.date_input("Date de fin", key="end_date")
        
    headers = {"Authorization": f"Bearer {token}"}

    # Déclencheurs
    try:
        trigger_response = requests.get(f"{API_URL}/triggers/", params={"user_id": user_id}, headers=headers)
        trigger_response.raise_for_status()
        all_triggers = trigger_response.json()
        user_triggers = [t['name'] for t in all_triggers if t.get('user_id') == user_id]
    except Exception as e:
        st.error(f"Erreur lors du chargement des déclencheurs : {e}")
        user_triggers = []

    st.multiselect("Déclencheurs", user_triggers, key="selected_triggers")

    # Réactions
    try:
        reaction_response = requests.get(f"{API_URL}/reactions/", params={"user_id": user_id}, headers=headers)
        reaction_response.raise_for_status()
        all_reactions = reaction_response.json()
        user_reactions = [r['name'] for r in all_reactions if r.get('user_id') == user_id]
    except Exception as e:
        st.error(f"Erreur lors du chargement des réactions : {e}")
        user_reactions = []

    st.multiselect("Réactions", user_reactions, key="selected_reactions")

    # Intensité
    st.multiselect("Intensité", [1, 2, 3, 4, 5], key="selected_severities")

    # Résultats
    results = []

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        if st.button("Rechercher"):
            payload = {
                "query": st.session_state.query_text,
                "start_date": str(st.session_state.start_date),
                "end_date": str(st.session_state.end_date),
                "triggers": st.session_state.selected_triggers,
                "reactions": st.session_state.selected_reactions,
                "severities": st.session_state.selected_severities
            }

            try:
                response = requests.post(f"{API_URL}/search/", headers=headers, json=payload)
                response.raise_for_status()
                results = response.json()
                st.success(f"{len(results)} résultats trouvés")

                # Afficher les résultats dans un tableau
                if results:
                    df = pd.DataFrame(results)
                    df["triggers"] = df["triggers"].apply(lambda x: ", ".join(x))
                    df["reactions"] = df["reactions"].apply(lambda x: ", ".join(x))
                    
                    df = df.rename(columns={
                        "severity": "Intensité",
                        "reactions": "Réaction",
                        "triggers": "Déclencheur",
                        "comment": "Commentaire",
                        "entry_date": "Date"
                    })

                    # Option de téléchargement des résultats en CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger en CSV",
                        data=csv,
                        file_name="resultats_observations.csv",
                        mime="text/csv"
                    )

            except Exception as e:
                st.error(f"Erreur lors de la recherche : {e}")

    with col4:
        if st.button("Réinitialiser"):
            st.session_state["reset_triggered"] = True
            st.rerun()

    # Sortie du tableau après la colonne, pour l'afficher plus large
    if results:
        st.dataframe(df, use_container_width=True)  # Affiche à la fin et occupe toute la largeur
