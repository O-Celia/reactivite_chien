# Application de suivi de réactivité pour chiens

## 1. Présentation générale

### 1.1. Contexte

Ce projet a été conçu pour répondre à un besoin personnel : suivre les comportements réactifs des chiens déclenchés par des facteurs externes (ex. : bruits, autres animaux, humains, etc.). Ce projet vise à concevoir une application pour suivre ces déclencheurs et leur intensité, ainsi que l’état émotionnel du chien, pour observer des tendances via des tableaux de bord et identifier des pistes d’amélioration.
Ce projet est destiné à un usage personnel et mis en place pour l'observation de mon chien et de celui d'une amie. L'application est donc à ce jour prévue pour une utilisation limitée. L’application a pour but d'être utilisée sur PC et mobile.

### 1.2. Objectifs

- Suivre les déclencheurs (événements stressants) et leur intensité.
- Enregistrer l’état émotionnel quotidien du chien (via des adjectifs prédéfinis).
- Offrir une visualisation claire et intuitive via un calendrier et des graphiques.
- Intégrer un dashboard Power BI pour l’analyse approfondie
- Permettre la recherche avancée via Elasticsearch dans la base de données.
- Garantir un accès simple et gratuit à l’application.
- Appliquer des outils DevOps ((CI/CD, containerisation, sécurité, IaC).
- Préparer l’extension cloud native pour un futur déploiement.

### 1.3. Exemple de scénario utilisateur

L'utilisateur se connecte à l’application sur son smartphone. Il saisit qu’aujourd’hui, son chien a réagi à un autre chien (intensité élevée) et semblait agité. En fin de semaine, il consulte le dashboard pour voir les déclencheurs les plus fréquents.

### 1.4 MVP (Version 1) :

- Authentification simple
- Saisie manuelle des déclencheurs
- Calendrier avec visualisation journalière
- Dashboard Power BI en local

## 2. Spécifications fonctionnelles

### 2.1. Fonctionnalités principales

**Authentification :**
- Création de compte utilisateur avec mot de passe chiffré.
- Authentification via JSON Web Tokens (JWT).
- Gestion des sessions côté API FastAPI.

**Gestion des déclencheurs :**
- Déclencheurs par défauts inclus pour simplifier le démarrage.
- Liste des déclencheurs personnalisables pour chaque utilisateur (ajout, modification, suppression).

**Saisie quotidienne :**
- Sélection des déclencheurs du jour et leur intensité (léger, moyen, élevé).
- Sélection des adjectifs émotionnels du jour (pré-remplis ou ajoutés) : fatigué, stressé, normal, heureux, malade, agressif.
- Calendrier interactif pour consulter et enregistrer les données.

**Visualisation des données :**
- Calendrier interactif avec affichage visuel des données (icônes ou d’indicateurs colorés)
- Détail de chaque journée accessible via clic.
- Page Analytics :
    - Fréquence et intensité des déclencheurs.
    - Répartition des adjectifs émotionnels.
    - Évolution temporelle.
    - Graphiques Streamlit (Plotly ou Matplotlib).
    - Ajout d'un lien Web PowerBI pour avoir des visualisations interactives disponibles.

**Recherche intelligente :**
- Recherche via Elasticsearch : filtres sur les déclencheurs, adjectifs, intensité et dates.
- Interface simple type barre de recherche + filtres.

**Multi-plateforme :**
- Application utilisable sur ordinateur et mobile (navigateur web).

### 2.2. Contraintes fonctionnelles

- Application gratuite à concevoir et à utiliser.
- Données sécurisées et accessibles uniquement à l’utilisateur.
- Interface simplifiée, intuitive.

## 3. Spécifications techniques

### 3.1. Technologies choisies

**Backend :**
- Langage : Python.
- Framework : FastAPI pour gérer les API REST.
- Base de données : SQLite (locale, légère, adaptée aux petits volumes de données).
- Authentification : JWT via `python-jose`).
- ORM : SQLAlchemy

**Frontend :**
- Streamlit pour une interface utilisateur interactive.

**Infrastructure :**
- Exécution locale via Streamlit.
- Docker pour portabilité.
- k3s pour futur déploiement (V2).
- Ingress : Traefik pour gérer l’exposition des services FastAPI/Streamlit sur le cluster Kubernetes (V2).
- Possibilité d’hébergement sur Oracle Cloud Free Tier (V2).
- Possibilité d'intégrer un certificat SSL pour de l'HTTPS (V3).

**Analyse de données :**
- Graphiques Plotly/Matplotlib pour visualisations des données.
- PowerBI Service pour l'ajout d'un lien Web avec graphiques interactifs.
- Elasticsearch pour la recherche intelligente (via Docker).

**DevOps :**
- GitHub Actions : pipelines CI/CD pour automatiser tests et déploiement avant mise en production.
- Docker : conteneurisation de l’application pour portabilité.
- Terraform : Infrastructure as Code pour configurer l’hébergement.
- Kubernetes/k3s : Orchestration avec fichiers YAML et Helm Charts.

**Sécurité :**
- Gestion des secrets et variables d’environnement avec des fichiers .env.
- OWASP pour audit de sécurité.
- Pytest dans GitHub Actions

## 4. Interface utilisateur

### 4.1. Page d’accueil

- Formulaire de connexion et d’inscription.

### 4.2. Page de gestion des déclencheurs

- Liste des déclencheurs existants.
- Ajout / modification / suppression d'un nouveau déclencheur.
- Utilisation possible d’émojis pour illustrer.

### 4.3. Page de saisie quotidienne

- Calendrier interactif avec sélection de date.
- Sélection des déclencheurs du jour (avec intensité).
- Sélection des adjectifs émotionnels.

### 4.4. Page analytics

**Graphiques générés avec Plotly :**
- Histogramme des déclencheurs (par intensité).
- Diagramme circulaire des adjectifs (répartition).
- Graphique linéaire des tendances temporelles.
- Jauge ou cercle (%) de réactivité mensuelle.

**Recherche avancée via Elasticsearch :**
- champ de recherche textuelle,
- filtres temporels (plages de dates),
- filtres par mots-clés/intensité.

## 5. Étapes détaillées de mise en place

### 5.1. Préparation

**Installation des outils :**
- Python, pip, et modules nécessaires : fastapi, uvicorn, sqlalchemy, streamlit, vault-cli (V2).
- Power BI Desktop.
- Docker
- Elasticsearch

**Planification BDD :**
- Utilisateurs
- Déclencheurs
- Saisies journalières
- Adjectifs émotionnels.

### 5.2. Développement du backend (API REST)

**Mise en place de FastAPI :**
- Créer un projet FastAPI avec uvicorn pour exécuter le serveur localement.
- Configurer les routes REST :
    - /register : inscription utilisateur.
    - /login : retour d'un JWT.
    - /triggers : CRUD sur les déclencheurs.
    - /daily-entry : enregistrement des données journalières.
    - /analytics : récupération de données agrégées.
    - /search : requête Elasticsearch.

**Base de données SQLite :**
- Modéliser les tables avec SQLAlchemy :
    - User : identifiants utilisateur.
    - Trigger : liste des déclencheurs (nom, description).
    - DailyEntry : données journalières (date, intensité, adjectifs, utilisateur lié).
    - Reaction : humeur du chien dans la journée.
- Initialiser la base et inclure des déclencheurs par défaut.

**Sécurisation des API :**
- Ajouter des tokens JWT pour gérer les sessions utilisateurs.
- Stocker les secrets et clés dans Vault (V2).

**Intégration Elasticsearch :**
- Docker local.
- Indexation automatique des nouvelles saisies.
- Requêtes filtrées exposées via /search.

### 5.3. Développement du frontend (Interface utilisateur Streamlit)

**Structure de l'app :**
- Créer un script principal app.py.
- Implémenter les pages principales :
    - Accueil/Connexion
    - Calendrier
    - Saisie
    - Analytics
    - Recherche

**Appels API :**
- Connexion à FastAPI via requêtes HTTP (lib requests).
- Stockage local du JWT pour les appels sécurisés.

### 5.4. Analyse des données (Power BI)

- Création de dashboards dans Power BI.
- Publication de graphiques avec Matplotlib ou Plotly.
- Graphiques interactifs sur PowerBi Service.
- Export PDF des données.

### 5.5. Automatisation DevOps

**Conteneurisation :**
- Écrire un Dockerfile pour le backend et l’interface Streamlit.
- Construire et tester l’image localement.

**Pipeline CI/CD :**
- Configurer GitHub Actions pour :
    - Lancer des tests unitaires (FastAPI).
    - Construire une image Docker et déployer sur le cloud.

## 6. Application V2

### 6.1. Automatisation DevOps

**Infrastructure as Code :**
- Utilisation de Terraform pour automatiser la création et la gestion des ressources cloud sur Oracle Cloud Infrastructure (OCI).
- Provisionnement automatisé :
    - Déploiement de machines virtuelles ou services managés.
    - Création des ressources réseau nécessaires (VPC, Load Balancer, etc.).
    - Configuration du cluster K3s pour l’orchestration des conteneurs.
- Intégration de Vault pour la gestion centralisée et sécurisée des secrets (API keys, tokens JWT, identifiants DB…).

### 6.2. Déploiement cloud

**Architecture cloud-native sur Oracle Cloud :**
- Déploiement de l’application dans un cluster K3s :
    - Backend (FastAPI) et Frontend (Streamlit) déployés dans des conteneurs gérés par K3s.
    - Base de données migrée de SQLite vers Oracle Database pour assurer une meilleure scalabilité et intégration avec l’écosystème OCI.
    - Configuration des services via des fichiers Helm Charts ou manifests YAML.
    - Utilisation d’Ingress Controller (Traefik) pour gérer les points d’entrée et le routage HTTP/HTTPS.
- Alerting possible en cas d’erreurs critiques ou d’indisponibilité.

### 6.3. Monitoring

- Mise en place d’un système de supervision avec :
    - Prometheus pour collecter les métriques des conteneurs (CPU, mémoire, erreurs, etc.).
    - Grafana pour visualiser les métriques et détecter les anomalies ou baisses de performance via des dashboards dynamiques.
- Grafana

## 7. Maintenance et évolutions futures

**Surveillance continue :**
- Analyse des logs applicatifs et système via les outils natifs d'Oracle Cloud et Grafana.
- Mise en place d’un système de rotation et d’archivage des logs.

**Améliorations possibles :**
- Compatible PC et smartphone
- Ajouter des notifications (ex. : rappel de saisie quotidienne).
- Étendre l’analyse avec des graphiques supplémentaires.
- Ajouter une page Médicaments (rappel, liste de médicaments, dosage).
- Ajouter une page suivi des déplacements : carte sur laquelle l'utilisateur signale le début et la fin d'une balade, afin d'évaluer si la distance ou la durée de la balade augmente ou diminue.
