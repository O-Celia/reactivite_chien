# Application de suivi de réactivité pour chiens

## 1. Présentation générale

### 1.1. Contexte

Mon chien a des comportements réactifs déclenchés par des facteurs externes (ex. : bruits, autres animaux). Ce projet vise à concevoir une application personnelle pour suivre ces déclencheurs et leur intensité, ainsi que l’état émotionnel du chien, pour observer des tendances via des tableaux de bord et identifier des pistes d’amélioration.
Ce projet est mis en place pour l'observation de mon chien et de celui d'une amie. L'application est donc à ce jour prévue pour une utilisation limitée. L’application a pour but d'être utilisée sur PC et mobile.

### 1.2. Objectifs

- Suivre les déclencheurs (événements stressants) et leur intensité.
- Enregistrer l’état émotionnel quotidien du chien (via des adjectifs prédéfinis).
- Offrir une visualisation claire et intuitive via un calendrier interactif et des graphiques.
- Offrir une possibilité de recherche avancée dans la base de données.
- Garantir un accès simple et gratuit à l’application, utilisable sur ordinateur et smartphone.
- Appliquer des outils DevOps pour automatiser le déploiement et la gestion des secrets.

### 1.3. Exemple de scénario utilisateur

L'utilisateur se connecte à l’application sur son smartphone. Il saisit qu’aujourd’hui, son chien a réagi à un autre chien (intensité élevée) et semblait agité. En fin de semaine, elle consulte le dashboard pour voir les déclencheurs les plus fréquents.

#### 1.4 MVP (Version 1) :

- Authentification simple
- Saisie manuelle des déclencheurs
- Calendrier avec visualisation journalière
- Dashboard Power BI en local

## 2. Spécifications fonctionnelles

### 2.1. Fonctionnalités principales

Fonctionnalités utilisateur :

Création de compte utilisateur :
- Possibilité de créer un compte unique pour l’application.
- Authentification basique (nom d’utilisateur/mot de passe).
- Gestion des comptes via FastAPI.

Gestion des déclencheurs :
- Déclencheurs par défauts inclus pour simplifier le démarrage.
- Liste des déclencheurs personnalisables pour chaque utilisateur (ajout, modification).

Saisie quotidienne :
- Sélectionner les déclencheurs du jour et leur intensité (léger, moyen, élevé).
- Ajouter des adjectifs décrivant l’état émotionnel du chien : Pré-suggestions (fatigué, stressé, normal, heureux, malade, agressif) ou ajouts manuels à la liste proposée.
- Calendrier interactif pour consigner les données journalières

Visualisation des données :
- Page calendrier interactif :</br>
Permet d’afficher les données journalières sous forme d’icônes ou d’indicateurs colorés. </br>
Cliquer sur une date ouvre une fenêtre de détails.
- Page analytics :</br>
Dashboard (avec des visuels PowerBI exportés en PNG/JPEG ou utilisation de Plotly ou Matplotlib dans Streamlit pour remplacer certains dashboard) pour analyser :
    - Fréquence et intensité des déclencheurs.
    - Répartition des adjectifs sur une période donnée.
    - Tendances temporelles (amélioration/dégradation).

Ajout d'un lien Web PowerBI pour avoir des visualisations interactives disponibles (l'ajout direct sur l'application nécessite PowerBI Embedded, qui est payant).

Recherche intelligente : </br>
Une fonctionnalité de recherche avancée permettra de filtrer les saisies par mots-clés, intensité, humeur ou plage de dates. L’utilisateur pourra ainsi retrouver des situations similaires ou observer des cas spécifiques. Cette recherche sera alimentée par Elasticsearch.

Multi-plateforme :
- Application utilisable sur ordinateur (navigateur web) et smartphone.

### 2.2. Contraintes fonctionnelles

L’application doit être gratuite à concevoir et à utiliser. </br>
Les données doivent être sécurisées et accessibles uniquement à l’utilisateur.</br>
Interface simplifiée pour une utilisation intuitive. </br>
Compatible mobile et PC, avec hébergement cloud.

## 3. Spécifications techniques

### 3.1. Technologies choisies

Backend :
- Langage : Python.
- Framework : FastAPI pour gérer les API REST.
- Base de données : SQLite (locale, légère, adaptée aux petits volumes de données) ou MySQL (familiarité d'utilisation).
- Authentification : Auth0 (authentification OAuth2 moderne et sécurisée, intégrée avec FastAPI via `authlib` ou `python-jose`).
- Stockage fichiers : si l'application doit permettre à terme le dépôt ou la lecture de fichiers (ex. : captures d’écran, exports de graphiques, journaux), un stockage séparé sera nécessaire (MinIO, volume Docker local, ou volume Kubernetes).

Frontend :
- Streamlit pour une interface utilisateur interactive et développée en Python.

Infrastructure :
- Hébergement local pour un usage personnel sur ordinateur (Flask/Streamlit exécuté en localhost).
- Possibilité d’hébergement cloud gratuit (Oracle) si besoin de synchronisation entre plusieurs appareils, ou K3s avec raspberry pour maintenir l'application en ligne.
- Ingress Controller : Traefik pour gérer l’exposition des services FastAPI/Streamlit sur le cluster Kubernetes. Possibilité d’y intégrer un certificat SSL plus tard si HTTPS devient envisageable.

Outils d’analyse :
- Power BI Desktop pour créer des visualisations des données stockées dans la BDD.
- Intégration des graphiques Power BI dans la page analytics.
- Elasticsearch pour indexer et rechercher efficacement les saisies journalières (déclencheurs, adjectifs, commentaires éventuels) avec ajout d'une fonctionnalité de recherche rapide par mots-clés, filtres (intensité, humeur, date, etc.) ou suggestions basées sur les données saisies.

DevOps :
- GitHub Actions : pipelines CI/CD pour automatiser tests et déploiement avant mise en production.
- Docker : conteneurisation de l’application pour portabilité.
- Terraform : Infrastructure as Code pour configurer l’hébergement.
- Kubernetes : Orchestration avec fichiers YAML et Helm Charts.

Sécurité :
- Gestion des secrets et variables d’environnement avec HashiCorp Vault ou fichiers .env.
- OWASP pour audit de sécurité.

## 4. Interface utilisateur

### 4.1. Page d’accueil

Formulaire de connexion et d’inscription.

### 4.2. Page de gestion des déclencheurs

Liste des déclencheurs existants. </br>
Bouton pour ajouter un nouveau déclencheur (nom + description). </br>
Options pour modifier ou supprimer des déclencheurs (choix d'emojis éventuellement).

### 4.3. Page de saisie quotidienne

Calendrier interactif :
- Sélection d’une date pour saisir des données.

Formulaire de saisie :
- Liste des déclencheurs avec cases à cocher pour sélectionner ceux qui se sont produits.
- Choix de l’intensité (léger, moyen, élevé).
- Liste d’adjectifs de l'humeur du chien prédéfinis avec sélection multiple.

### 4.4. Page analytics

Graphiques générés avec Power BI :
- Histogramme des déclencheurs (par intensité).
- Diagramme circulaire des adjectifs (répartition).
- Graphique linéaire des tendances temporelles.
- Jauge ou cercle (%) de réactivité sur le mois

Recherche avancée via Elasticsearch : </br>
Une zone de recherche sera ajoutée à la page analytics, permettant à l’utilisateur d’explorer ses données personnelles avec une interface simple de type moteur de recherche. Cette fonctionnalité exploitera Elasticsearch pour offrir une recherche rapide, tolérante aux fautes de frappe, et filtrable (par date, intensité, adjectifs, déclencheurs). L’interface proposera :
- un champ de recherche textuelle,
- des filtres temporels (plages de dates),
- des filtres par mots-clés/intensité.

Les résultats s’afficheront sous forme de liste ou de résumé visuel (table ou graphique simple), et permettront d’identifier rapidement des patterns ou cas spécifiques.

## 5. Étapes détaillées de mise en place

### 5.1. Préparation

Installation des outils :
- Python 3.11, pip, et modules nécessaires : fastapi, uvicorn, sqlalchemy, streamlit, vault-cli.
- Power BI Desktop.
- Docker
- Elasticsearch

Planification des fonctionnalités :
- Définir la structure de la base de données (table utilisateurs, déclencheurs, saisies journalières).
- Préparer un design préliminaire pour le calendrier et les tableaux de bord.

### 5.2. Développement du backend (API REST)

Mise en place de FastAPI :
- Créer un projet FastAPI avec uvicorn pour exécuter le serveur localement.
- Configurer les routes REST :
    - /register : inscription utilisateur.
    - /login : connexion et authentification.
    - /triggers : gestion des déclencheurs.
    - /mood : gestion de l'humeur du chien.
    - /daily-entry : enregistrement des données journalières.
    - /analytics : affichage des visualisations.

Base de données SQLite :
- Modéliser les tables avec SQLAlchemy :
    - User : identifiants utilisateur.
    - Trigger : liste des déclencheurs (nom, description).
    - DailyEntry : données journalières (date, intensité, adjectifs, utilisateur lié).
    - Adjectives : humeur du chien dans la journée.
- Initialiser la base et inclure des déclencheurs par défaut.

Sécurisation des API :
- Ajouter des tokens JWT pour gérer les sessions utilisateurs.
- Stocker les secrets et clés dans Vault.

Intégration Elasticsearch :
- Installer et configurer un conteneur Elasticsearch via Docker.
- Créer une fonction de synchronisation entre les données de la base SQL et l’index Elasticsearch (ex. : chaque nouvelle saisie ou modification alimente aussi l’index).
- Exposer une API /search permettant de requêter Elasticsearch à partir de Streamlit.
- Indexer les champs suivants : date, adjectifs, déclencheurs, intensité, commentaire libre (si ajouté).

### 5.3. Développement du frontend (Interface utilisateur)

Mise en place de Streamlit :
- Créer un script principal app.py.
- Implémenter les pages principales :
    - Page Calendrier : formulaire interactif pour saisir ou consulter les données.
    - Page Analytics : intégrer les visualisations Power BI et une barre de recherche.

Intégration des fonctionnalités :
- Appeler les API FastAPI pour récupérer et enregistrer les données.
- Construire un formulaire utilisateur intuitif pour gérer les déclencheurs et adjectifs.

### 5.4. Analyse des données (Power BI)

Création des tableaux de bord :
- Connecter Power BI à la BDD.
- Concevoir :
    - Histogramme des déclencheurs (par intensité).
    - Diagramme circulaire pour les adjectifs (répartition).
    - Graphique linéaire des tendances temporelles.
    - Jauge ou cercle (%) de réactivité sur le mois

Publication locale :
- Exporter les graphiques en HTML ou JPG.

### 5.5. Automatisation DevOps

Pipeline CI/CD :
- Configurer GitHub Actions pour :
    - Lancer des tests unitaires (FastAPI).
    - Construire une image Docker et déployer sur le cloud.

Infrastructure as Code :
- Utiliser Terraform pour configurer le cloud :
    - Créer dynamiquement les instances nécessaires.
    - Intégrer les secrets via Vault.

Conteneurisation :
- Écrire un Dockerfile pour le backend et l’interface Streamlit.
- Construire et tester l’image localement.

### 5.6. Déploiement

Configuration cloud :
- Créer une application sur le cloud choisi et lier le dépôt GitHub.
- Déployer via Docker ou le CLI.

Tests finaux :
- Vérifier le fonctionnement sur ordinateur et smartphone.
- Tester les visualisations Power BI et la saisie dans le calendrier.

## 6. Maintenance et évolutions futures

Surveillance : Utiliser les logs du cloud pour surveiller les erreurs. </br>
Améliorations possibles :
- Ajouter des notifications (ex. : rappel de saisie quotidienne).
- Étendre l’analyse avec des graphiques supplémentaires.
- Migrer vers une base de données plus robuste (PostgreSQL) si le volume augmente.
- Ajouter une page Médicaments (rappel, liste de médicaments, dosage).
- Ajouter une page suivi des déplacements : carte sur laquelle l'utilisateur signale le début et la fin d'une balade, afin d'évaluer si la distance ou la durée de la balade augmente ou diminue.
