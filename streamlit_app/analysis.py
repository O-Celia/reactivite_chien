import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import calendar

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "db.sqlite3")

def app():
    st.title("Analyses")

    # Connexion à la base de données
    conn = sqlite3.connect(DB_PATH)
    
    st.sidebar.title("Filtrer par période")
    periode = st.sidebar.selectbox(
        "Choisissez la période à afficher :",
        ("Toutes les données", "Cette année", "Ce mois", "Cette semaine", "Personnalisée")
    )

    selected_year = None
    selected_month = None

    where_clause = ""
    if periode == "Cette année":
        where_clause = "WHERE strftime('%Y', entry_date) = strftime('%Y', 'now')"
    elif periode == "Ce mois":
        where_clause = "WHERE strftime('%Y-%m', entry_date) = strftime('%Y-%m', 'now')"
    elif periode == "Cette semaine":
        where_clause = """
        WHERE strftime('%Y-%W', entry_date) = strftime('%Y-%W', 'now')
        """
    elif periode == "Personnalisée":
        year = st.sidebar.selectbox("Choisissez l'année", [None] + list(range(2000, datetime.now().year + 1)))
        month = st.sidebar.selectbox("Choisissez le mois", [None] + list(range(1, 13)))
        week_of_month = st.sidebar.selectbox("Choisissez la semaine du mois (1 à 4)", [None, 1, 2, 3, 4])
        
        selected_year = year
        selected_month = month

        filters = []
        if year:
            filters.append(f"strftime('%Y', entry_date) = '{year}'")
        if month:
            filters.append(f"strftime('%m', entry_date) = '{month:02d}'")
        if week_of_month:
            # Calcul semaine du mois : on prend le jour du mois, le divise par 7 et arrondit
            filters.append(f"CAST(strftime('%d', entry_date) AS INTEGER) BETWEEN {(week_of_month - 1) * 7 + 1} AND {week_of_month * 7}")

        if filters:
            where_clause = "WHERE " + " AND ".join(filters)

    # sinon (Toutes les données), le where_clause reste vide

    # 1. Nombre de déclenchements par intensité
    st.subheader("Nombre de déclenchements par intensité")
    query1 = f"""
    SELECT t.name AS trigger, d.severity
    FROM daily_entries d
    JOIN daily_entry_triggers det ON d.id = det.entry_id
    JOIN triggers t ON t.id = det.trigger_id
    {where_clause}
    """
    df1 = pd.read_sql_query(query1, conn)
    df1["severity"] = df1["severity"].astype(str)
    
    df1 = df1.rename(columns={
        "trigger": "Déclencheur",
        "severity": "Intensité"
    })

    custom_colors = {
        "1": "#a8dadc",  # bleu très clair
        "2": "#74c69d",  # vert doux
        "3": "#f9c74f",  # jaune
        "4": "#f9844a",  # orange
        "5": "#f94144",  # rouge foncé
    }
    if not df1.empty:
        fig1 = px.histogram(
            df1,
            x="Déclencheur",
            color="Intensité",
            barmode="stack",
            color_discrete_map=custom_colors,
            category_orders={"Intensité": ["1", "2", "3", "4", "5"]}
        )
        fig1.update_layout(
            xaxis_title="Déclencheur",
            yaxis_title="Nombre d'occurrences",
            legend_title="Intensité",
            bargap=0.2,
            template="plotly_white"
        )
        st.plotly_chart(fig1)
    else:
        st.info("Pas de données disponibles pour les déclencheurs.")

    # 2. Diagramme circulaire des réactions
    st.subheader("Répartition des réactions")
    query2 = f"""
    SELECT 
        r.name AS reaction,
        COUNT(*) AS count,
        GROUP_CONCAT(DISTINCT t.name) AS triggers
    FROM daily_entry_reactions der
    JOIN reactions r ON der.reaction_id = r.id
    JOIN daily_entries d ON der.entry_id = d.id
    JOIN daily_entry_triggers det ON d.id = det.entry_id
    JOIN triggers t ON det.trigger_id = t.id
    {where_clause}
    GROUP BY r.name
    """
    
    df2 = pd.read_sql_query(query2, conn)
    df2 = df2.rename(columns={
        "reaction": "Réaction",
        "count": "Occurrences",
        "triggers": "Déclencheurs"
    })

    if not df2.empty:
        fig2 = px.pie(
            df2, 
            names="Réaction", 
            values="Occurrences", 
            hover_data=["Déclencheurs"]
        )
        fig2.update_traces(textinfo='percent')
        st.plotly_chart(fig2)
    else:
        st.info("Pas de données disponibles pour les réactions.")

    # 3. Graphique de tendance temporelle
    # Ajoutez cette partie dans la section de filtrage pour la tendance temporelle
    st.subheader("Tendance de la sévérité dans le temps")

    # Sélection du déclencheur
    selected_trigger = st.sidebar.selectbox(
        "Choisissez un déclencheur pour le graphique 'Tendance de la sévérité dans le temps' :",
        ["Tous les déclencheurs"] + df1["Déclencheur"].unique().tolist()
    )

    conditions = []

    # Ajoute les conditions de période (from where_clause) si elles existent
    if where_clause:
        # Supprimer le mot-clé 'WHERE' pour le réutiliser proprement ensuite
        conditions.append(where_clause.replace("WHERE", "").strip())

    # Ajoute la condition de déclencheur si un spécifique est choisi
    if selected_trigger != "Tous les déclencheurs":
        conditions.append(f"t.name = '{selected_trigger}'")

    # Assemble les conditions finales
    final_where = ""
    if conditions:
        final_where = "WHERE " + " AND ".join(conditions)

    # Construction finale de la requête
    query3 = f"""
    SELECT 
        d.entry_date,
        AVG(d.severity) AS moyenne_intensité,
        GROUP_CONCAT(DISTINCT t.name) AS déclencheurs
    FROM daily_entries d
    LEFT JOIN daily_entry_triggers det ON d.id = det.entry_id
    LEFT JOIN triggers t ON t.id = det.trigger_id
    """

    # Construire dynamiquement les conditions
    conditions = []

    if where_clause:
        # where_clause contient déjà WHERE ...
        conditions.append(where_clause.replace("WHERE", "").strip())

    if selected_trigger != "Tous les déclencheurs":
        conditions.append(f"t.name = '{selected_trigger}'")

    if conditions:
        query3 += "WHERE " + " AND ".join(conditions)

    query3 += """
    GROUP BY d.entry_date
    ORDER BY d.entry_date
    """

    # Exécution de la requête
    df3 = pd.read_sql_query(query3, conn)

    # Affichage du graphique si les données sont présentes
    if not df3.empty:
        df3 = df3.rename(columns={
            "entry_date": "Date",
            "moyenne_intensité": "Intensité moyenne",
            "déclencheurs": "Déclencheurs"
        })

        fig3 = px.line(
            df3,
            x="Date",
            y="Intensité moyenne",
            hover_data={"Déclencheurs": True},
            markers=True
        )
        fig3.update_layout(
            xaxis_title="Date",
            yaxis_title="Intensité moyenne",
            legend_title="Légende",
            template="plotly_white"
        )
        st.plotly_chart(fig3)
    else:
        st.info("Pas de données disponibles pour la tendance temporelle.")

    # st.subheader("Tendance de la sévérité dans le temps")

    # query3 = f"""
    # SELECT 
    #     d.entry_date,
    #     AVG(d.severity) AS moyenne_intensité,
    #     GROUP_CONCAT(DISTINCT t.name) AS déclencheurs
    # FROM daily_entries d
    # LEFT JOIN daily_entry_triggers det ON d.id = det.entry_id
    # LEFT JOIN triggers t ON t.id = det.trigger_id
    # {where_clause}
    # GROUP BY d.entry_date
    # ORDER BY d.entry_date
    # """

    # df3 = pd.read_sql_query(query3, conn)

    # if not df3.empty:
    #     df3 = df3.rename(columns={
    #         "entry_date": "Date",
    #         "moyenne_intensité": "Intensité moyenne",
    #         "déclencheurs": "Déclencheurs"
    #     })

    #     fig3 = px.line(
    #         df3,
    #         x="Date",
    #         y="Intensité moyenne",
    #         hover_data={"Déclencheurs": True},
    #         markers=True
    #     )
    #     fig3.update_layout(
    #         xaxis_title="Date",
    #         yaxis_title="Intensité moyenne",
    #         legend_title="Légende",
    #         template="plotly_white"
    #     )
    #     st.plotly_chart(fig3)
    # else:
    #     st.info("Pas de données disponibles pour la tendance temporelle.")
    
    # 4. Jauge de réactivité mensuelle avec comparaison
    st.subheader("Réactivité du mois sélectionné (%)")

    # Détermination du mois sélectionné
    if periode == "Personnalisée":
        year = st.session_state.get("selected_year", datetime.now().year)
        month = st.session_state.get("selected_month", datetime.now().month)
        if selected_year:
            year = selected_year
            st.session_state["selected_year"] = selected_year
        if selected_month:
            month = selected_month
            st.session_state["selected_month"] = selected_month
    else:
        year = datetime.now().year
        month = datetime.now().month

    selected_ym = f"{year}-{month:02d}"

    # Mois précédent
    if month == 1:
        previous_year = year - 1
        previous_month = 12
    else:
        previous_year = year
        previous_month = month - 1

    previous_ym = f"{previous_year}-{previous_month:02d}"

    # Mois en français
    mois_fr = {
        1: "janvier", 2: "février", 3: "mars", 4: "avril",
        5: "mai", 6: "juin", 7: "juillet", 8: "août",
        9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
    }
    mois_nom = mois_fr[month]
    mois_precedent_nom = mois_fr[previous_month]

    # Requêtes SQL
    query_current = f"""
    SELECT COUNT(*) as total, 
        SUM(CASE WHEN severity >= 4 THEN 1 ELSE 0 END) as high_severity
    FROM daily_entries
    WHERE strftime('%Y-%m', entry_date) = '{selected_ym}'
    """

    query_previous = f"""
    SELECT COUNT(*) as total, 
        SUM(CASE WHEN severity >= 4 THEN 1 ELSE 0 END) as high_severity
    FROM daily_entries
    WHERE strftime('%Y-%m', entry_date) = '{previous_ym}'
    """

    df_current = pd.read_sql_query(query_current, conn)
    df_previous = pd.read_sql_query(query_previous, conn)

    # Calculs et affichage
    if not df_current.empty and df_current['total'][0] > 0:
        current_ratio = df_current['high_severity'][0] / df_current['total'][0] * 100

        if not df_previous.empty and df_previous['total'][0] > 0:
            previous_ratio = df_previous['high_severity'][0] / df_previous['total'][0] * 100
            delta_text = f" (vs. {mois_precedent_nom})"
        else:
            previous_ratio = 0
            delta_text = f" (vs. {mois_precedent_nom} : NA)"

        titre_jauge = f"Proportion d'entrées à haute intensité (≥ 4) pour {mois_nom}{delta_text}"

        fig4 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_ratio,
            number={'suffix': " %"},
            delta={
                'reference': previous_ratio,
                'relative': False,
                'increasing': {'color': "red"},
                'decreasing': {'color': "green"}
            },
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 33], 'color': 'green'},
                    {'range': [33, 66], 'color': 'orange'},
                    {'range': [66, 100], 'color': 'red'},
                ],
            }
        ))
        fig4.update_layout(title=titre_jauge)
        st.plotly_chart(fig4)
    else:
        st.info(f"Pas de données pour le mois sélectionné ({mois_nom}).")

    conn.close()
