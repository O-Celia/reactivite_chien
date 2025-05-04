import streamlit as st
import requests
from streamlit_calendar import calendar
from datetime import datetime

def app():
        
    token = st.session_state.get("token", None)
    if not token:
        st.warning("Vous devez être connecté pour voir cette page.")
        st.stop()
    headers = {"Authorization": f"Bearer {token}"}
    
    st.title("Calendrier de réactivité")

    # Récupérer les entrées
    try:
        response = requests.get("http://localhost:8000/entry/", headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return

    # Transformer les données pour le calendrier
    events = []
    filtered_data = []
    
    for entry in data:
        reaction_text = ", ".join(entry["reactions"]) if isinstance(entry["reactions"], list) else entry["reactions"]
        trigger_text = ", ".join(entry["triggers"]) if isinstance(entry["triggers"], list) else entry["triggers"]

        if entry['severity'] in [1, 2]:
            background_color = '#4CAF50'  # Vert
        elif entry['severity'] == 3:
            background_color = '#FFA500'  # Orange
        else:
            background_color = '#F44336'  # Rouge
            
        date_str = entry["entry_date"]
        date_obj = datetime.fromisoformat(date_str)

        events.append({
            "title": f"{trigger_text}",
            "start": entry["entry_date"],
            "description": f"Réaction : {reaction_text}",
            "backgroundColor": background_color,
            "borderColor": background_color,
            "severity": entry['severity'],
            "ID" : entry["id"]
        })
        
        filtered_data.append({
            "date_obj": date_obj,
            "start": date_str,
            "title": trigger_text,
            "description": f"Réaction : {reaction_text}",
            "severity": entry["severity"],
            "backgroundColor": background_color,
            "ID": entry["id"]
        })

    # Configuration du calendrier
    calendar_options = {
        "initialView": "dayGridMonth",
        "locale": "fr",
    }

    calendar(events=events, options=calendar_options)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Sélecteur de mois uniquement pour filtrer l'expander
    available_years = sorted({e["date_obj"].year for e in filtered_data}) if filtered_data else [datetime.today().year]
    months = list(range(1, 13))
    month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Année", available_years, index=available_years.index(datetime.today().year))
    with col2:
        selected_month_num = st.selectbox("Mois", months, index=datetime.today().month - 1, format_func=lambda m: month_names[m - 1])

            
    # Affichage filtré dans l'expander
    with st.expander("Informations supplémentaires sous forme de liste"):
        filtered_events = [
            e for e in filtered_data
            if e["date_obj"].month == selected_month_num and e["date_obj"].year == selected_year
        ]

        if filtered_events:
            for event in filtered_events:
                color = event.get("backgroundColor", "#000000")
                st.markdown(
                    f"<span style='color:{color};'><strong>{event['start']}</strong></span> : {event['title']} ({event['severity']}/5) — {event['description']}, ID : {event['ID']}",
                    unsafe_allow_html=True
                )
        else:
            st.info("Aucune entrée pour le mois sélectionné.")
