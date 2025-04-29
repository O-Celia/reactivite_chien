import streamlit as st
import requests
from streamlit_calendar import calendar

def app():
    st.title("Calendrier de réactivité")

    # Appeler API pour récupérer les entrées
    try:
        response = requests.get("http://localhost:8000/entry/")
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return

    # Transformer les données pour le calendrier
    events = []
    for entry in data:
        reaction_text = ", ".join(entry["reactions"]) if isinstance(entry["reactions"], list) else entry["reactions"]
        trigger_text = ", ".join(entry["triggers"]) if isinstance(entry["triggers"], list) else entry["triggers"]

        if entry['severity'] in [1, 2]:
            background_color = '#4CAF50'  # Vert
        elif entry['severity'] == 3:
            background_color = '#FFA500'  # Orange
        else:
            background_color = '#F44336'  # Rouge

        events.append({
            "title": f"{trigger_text}",
            "start": entry["entry_date"],
            "description": f"Réaction : {reaction_text}",
            "backgroundColor": background_color,
            "borderColor": background_color,
            "severity": entry['severity'],
            "ID" : entry["id"]
        })

    #Configuration du calendrier
    calendar_options = {
        "initialView": "dayGridMonth",
        "locale": "fr",
    }

    calendar(events=events, options=calendar_options)

    st.markdown("---")
            
    with st.expander("Informations supplémentaires sous forme de liste"):
        for event in events:
            color = event.get("backgroundColor", "#000000")
            st.markdown(
                f"<span style='color:{color};'><strong>{event['start']}</strong></span> : {event['title']} ({event['severity']}/5) — {event['description']}, ID : {event['ID']}",
                unsafe_allow_html=True
            )
