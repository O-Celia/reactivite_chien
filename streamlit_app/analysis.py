import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import plotly.graph_objects as go

API_BASE_URL = "http://localhost:8000"

def app():
    st.title("Analyse de la réactivité")
    
    token = st.session_state.get("token")
    if not token:
        st.error("Vous devez être connecté pour voir les graphiques d'analyse.")
        return

    # Chargement des données via API FastAPI
    @st.cache_data
    def load_data():
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/entry/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            return df
        else:
            st.error("Erreur lors de la récupération des données depuis l'API.")
            return pd.DataFrame()

    df = load_data()
    df_all = df.copy()  # Pour garder toutes les données

    if 'entry_date' in df_all.columns:
        df_all['entry_date'] = pd.to_datetime(df_all['entry_date'], errors='coerce')

    if df.empty:
        st.warning("Aucune donnée à afficher.")
        st.stop()

    # Conversion des colonnes
    if 'entry_date' in df.columns:
        df['date'] = pd.to_datetime(df['entry_date'], errors='coerce')
    else:
        df['date'] = pd.NaT

    if 'triggers' in df.columns and df['triggers'].apply(lambda x: isinstance(x, str)).any():
        df['triggers'] = df['triggers'].apply(eval)

    # Filtrage temporel
    st.subheader("Filtrer les données")
    periode = st.selectbox("Période", [
        "Toutes les données", "Cette année", "Ce mois", "Cette semaine", "Personnalisé"
    ])

    today = datetime.today()

    if periode == "Cette année":
        df = df[df['date'].dt.year == today.year]
    elif periode == "Ce mois":
        df = df[(df['date'].dt.year == today.year) & (df['date'].dt.month == today.month)]
    elif periode == "Cette semaine":
        df = df[(df['date'].dt.year == today.year) & (df['date'].dt.isocalendar().week == today.isocalendar().week)]
    elif periode == "Personnalisé":
        selected_year = st.selectbox("Année", list(range(2000, today.year + 1))[::-1], index=0)
        month_filter = st.checkbox("Filtrer par mois")
        week_filter = st.checkbox("Filtrer par semaine")
        
        df = df[df['date'].dt.year == selected_year]
        
        if month_filter:
            mois_francais_liste = [
                "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
            ]
            selected_month = st.selectbox("Mois", list(range(1, 13)), format_func=lambda m: mois_francais_liste[m - 1])

            df = df[df['date'].dt.month == selected_month]

        if week_filter:
            selected_week = st.selectbox("Semaine du mois (1 à 4)", list(range(1, 5)))
            df['week_of_month'] = df['date'].apply(lambda d: (d.day - 1) // 7 + 1)
            df = df[df['week_of_month'] == selected_week]

    # Graphique 1 : Nombre de déclenchements par intensité
    st.subheader("Nombre de déclenchements et intensité des réactions")

    df_exploded = df.explode('triggers')
    df_counts = df_exploded.groupby(['triggers', 'severity']).size().reset_index(name='count')

    fig1 = px.bar(df_counts, x='triggers', y='count', color='severity', barmode='stack',
                labels={'count': 'Nombre d’occurrences', 'severity': 'Intensité'})
    fig1.update_layout(xaxis_title=None)

    st.plotly_chart(fig1, use_container_width=True)


    # Graphique 2 : Évolution de l'intensité moyenne des réactions dans le temps
    st.subheader("Évolution de l'intensité des réactions")
    df_exploded['date'] = pd.to_datetime(df_exploded['date'], errors='coerce')
    df_exploded = df_exploded.dropna(subset=['date', 'severity'])
    df_exploded = df_exploded.dropna(subset=['severity'])

    # Regrouper par jour : intensité moyenne par date
    df_avg_severity = df_exploded.groupby('date')['severity'].mean().reset_index()

    if len(df_avg_severity) == 1:
        fig2 = go.Figure(data=go.Scatter(
            x=df_avg_severity['date'], 
            y=df_avg_severity['severity'], 
            mode='markers',  # Affiche uniquement les points
            marker=dict(color='blue', size=12)
        ))
    else:
        fig2 = px.line(df_avg_severity, x='date', y='severity', labels={'date': 'Date', 'severity': 'Intensité moyenne', 'reactions': 'Réaction'})
    st.plotly_chart(fig2, use_container_width=True)

    # Graphique 3 : Diagramme des réactions
    st.subheader("Répartition des types de réaction")
    df_exploded = df.explode('reactions')
    df_pie = df_exploded.groupby('reactions').agg(
        count=('reactions', 'count'),
        triggers_list=('triggers', lambda x: ', '.join(set(map(str, sum(x, [])))))
    ).reset_index()

    fig3 = px.pie(
        df_pie,
        names='reactions',
        values='count',
        labels={'reactions':'Réaction'},
        hover_data=['triggers_list']
    )

    fig3.update_traces(
        textinfo='percent',
        hovertemplate="<b>Occurrences: %{value}<br>Déclencheurs: %{customdata[0]}"
    )

    st.plotly_chart(fig3, use_container_width=True)
    
    # Graphique 4 : Jauge de réactivité mensuelle
    if not df.empty:
        # Déterminer la période sélectionnée par l'utilisateur
        if periode == "Personnalisé" and month_filter:
            selected_month_period = pd.Period(f"{selected_year}-{selected_month:02d}")
            previous_month_period = selected_month_period - 1
        else:
            # Par défaut : dernier mois présent dans les données filtrées
            selected_month_period = df_all['entry_date'].dt.to_period('M').max()
            previous_month_period = selected_month_period - 1

        # Filtrage des données pour les mois courant et précédent
        df_current = df_all[df_all['entry_date'].dt.to_period('M') == selected_month_period]
        df_previous = df_all[df_all['entry_date'].dt.to_period('M') == previous_month_period]

        def compute_proportion(df_month):
            if len(df_month) == 0:
                return 0
            return (df_month['severity'] >= 4).sum() / len(df_month)

        current_prop = compute_proportion(df_current)
        previous_prop = compute_proportion(df_previous)

        # Affichage dynamique du mois sélectionné
        mois_francais = {
            'January': 'Janvier', 'February': 'Février', 'March': 'Mars',
            'April': 'Avril', 'May': 'Mai', 'June': 'Juin',
            'July': 'Juillet', 'August': 'Août', 'September': 'Septembre',
            'October': 'Octobre', 'November': 'Novembre', 'December': 'Décembre'
        }

        mois_en = selected_month_period.to_timestamp().strftime('%B')
        annee = selected_month_period.to_timestamp().year
        mois_fr = f"{mois_francais[mois_en]} {annee}"

        st.subheader(f"Proportion d'entrées à haute intensité (≥ 4) pour {mois_fr} (comparé au mois précédent)")

        fig4 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_prop,
            number={'valueformat': '.1%', 'suffix': ''},
            delta={
                'reference': previous_prop,
                'valueformat': '.0%',
                'increasing': {'color': "red"},
                'decreasing': {'color': "green"}
            },
            gauge={
                'axis': {'range': [0, 1], 'tickformat': '.0%'},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 1/3], 'color': "green"},
                    {'range': [1/3, 2/3], 'color': "orange"},
                    {'range': [2/3, 1], 'color': "red"}
                ],
            }
        ))

        st.plotly_chart(fig4, use_container_width=True)
