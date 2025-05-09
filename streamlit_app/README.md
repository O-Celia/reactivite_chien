# Interface Streamlit

Cette application permet de gérer des observations avec un système de calendrier, de soumission, de modification, et de suppression des entrées. Elle se base sur une API qui interagit avec des déclencheurs, des réactions et des entrées d'observation.

## main_app.py

Ce script est le point d'entrée principal de l'application Streamlit. Il gère l'authentification des utilisateurs, la création de comptes, et l'interface de navigation entre les différentes pages de l'application.

Fonctionnalités :
- Connexion et inscription des utilisateurs via une API REST sécurisée.
- Gestion du premier login avec choix des déclencheurs et réactions par défaut.
- Navigation entre les modules de l’application à l’aide d’une barre latérale.
- Déconnexion sécurisée et gestion de session avec Streamlit.

Technologies : Streamlit, API RESTful (FastAPI), Python, Requests.

## Home.py

Ce script fournit l'interface principale de l'application de suivi de réactivité du chien. Il permet à l'utilisateur de se connecter, de consulter les statistiques rapides, et de naviguer dans les différentes sections de l'application.

Fonctionnalités :
- Affichage des informations de l'utilisateur après une connexion réussie.
- Affichage du nombre total d'entrées et de la date de la dernière entrée.
- Possibilité de consulter les dernières observations enregistrées.

Technologies : Streamlit, API Restful (requêtes GET), Python, Pandas.

## dataentry.py

Ce script permet à l'utilisateur d'ajouter de nouvelles observations via une interface Streamlit. L'utilisateur peut spécifier la date, le niveau de gravité, un commentaire, ainsi que les déclencheurs et réactions associés à l'observation.

Fonctionnalités :

- Ajouter une observation avec un déclencheur et une réaction existants ou nouveaux.
- Gérer les valeurs par défaut et la réinitialisation des champs.
- Authentification à l'aide d'un token (si non connecté, l'utilisateur est invité à se connecter).

Technologies : Streamlit, API Restful (requêtes GET, POST), Python.

## adminentry.py

Ce script permet de modifier ou de supprimer une observation existante. L'utilisateur entre l'ID de l'observation à modifier ou supprimer, puis peut mettre à jour ses informations.

Fonctionnalités :

- Modifier la date, l'intensité, les commentaires, les déclencheurs et réactions d'une observation existante.
- Supprimer une observation.
- Validation par un token d'authentification.

Technologies : Streamlit, API Restful (requêtes GET, PUT, DELETE), Python.

## calender.py

Ce script affiche un calendrier interactif pour visualiser les observations sous forme d'événements colorés en fonction de la gravité. L'utilisateur peut filtrer les événements par année et mois.

Fonctionnalités :

- Affichage des observations sous forme de calendrier avec couleurs selon la gravité.
- Filtrage par mois et année.
- Affichage des événements filtrés avec des informations supplémentaires sous forme de liste.

Technologies : Streamlit, API Restful (requêtes GET), calendrier interactif.

## research.py

Ce module permet aux utilisateurs de rechercher des observations précédemment enregistrées dans la base de données selon plusieurs critères.

Fonctionnalités :
- Filtres avancés : recherche par mots-clés, dates, déclencheurs, réactions et intensité.
- Affichage des résultats sous forme de tableau avec options de tri.
- Téléchargement des résultats filtrés au format CSV.
- Réinitialisation rapide de tous les filtres.

Technologies : Streamlit, API RESTful (requêtes POST et GET), Python, Pandas, Requests.

## analysis.py

Ce script permet de visualiser et analyser les données de réactivité du chien à travers différents graphiques interactifs.

Fonctionnalités :

- Affichage d'analyses basées sur les entrées de données : nombre de déclenchements selon l'intensité de la réaction, évolution de l'intensité des réactions, répartition des types de réactions, et jauge de réactivité mensuelle.
- Filtrage des données par période (année, mois, semaine, personnalisé).
- Visualisation des tendances dans le temps et des variations de la réactivité.

Technologies : Streamlit, Plotly, API Restful (requêtes GET), Python, Pandas.

## account.py

Ce script gère l'affichage et la modification des informations du compte utilisateur connecté. Il permet à l'utilisateur de voir ses informations personnelles, de les modifier et de supprimer son compte si nécessaire.

Fonctionnalités :
- Affichage des informations utilisateur récupérées depuis l'API.
- Modification du nom d'utilisateur, de l'email et du mot de passe.
- Suppression du compte utilisateur avec confirmation.

Technologies : Streamlit, API Restful (requêtes GET, PUT, DELETE), gestion de session.

## admin.py

Ce script permet de gérer les déclencheurs (triggers) et les réactions (reactions) via une interface d'administration. L'administrateur peut modifier, supprimer et ajouter des déclencheurs et réactions.

Fonctionnalités :
- Affichage de la liste des déclencheurs et des réactions.
- Modification du nom d'un déclencheur ou d'une réaction.
- Suppression d'un déclencheur ou d'une réaction.
- Ajout de nouveaux déclencheurs et réactions.

Technologies : Streamlit, API Restful (requêtes GET, PUT, DELETE, POST).
