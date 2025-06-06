# Application de suivi de réactivité pour chiens

## 1. Présentation générale

### 1.1. Contexte

Ce projet a été conçu pour répondre à un besoin personnel : suivre les comportements réactifs des chiens déclenchés par des facteurs externes (ex. : bruits, autres animaux, humains, etc.). Ce projet vise à concevoir une application pour suivre ces déclencheurs, ainsi que les réactions du chien et leur intensité, pour observer des tendances via des tableaux de bord et identifier des pistes d’amélioration.
Ce projet est destiné à un usage personnel et mis en place pour l'observation de mon chien et de celui d'une amie. L'application est donc à ce jour prévue pour une utilisation limitée. L’application a pour but d'être utilisée sur PC.

### 1.2. Objectifs

- Suivre les déclencheurs (événements stressants).
- Enregistrer l’état émotionnel quotidien du chien (via des réactions prédéfinies et leur intensité).
- Offrir une visualisation claire et intuitive via un calendrier et des graphiques.
- Intégrer un dashboard Power BI pour l’analyse approfondie
- Permettre la recherche avancée dans la base de données.
- Garantir un accès simple et gratuit à l’application.
- Préparer l’extension cloud native pour un futur déploiement,avec utilisation d'outils DevOps (CI/CD, conteneurisation, sécurité, monitoring).

### 1.3. Exemple de scénario utilisateur

L'utilisateur se connecte à l’application sur son PC. Il saisit qu’aujourd’hui, son chien a réagi à un autre chien en aboyant (intensité 3/5) et met en commentaire qu'il semblait agité en début de balade. En fin de semaine, il consulte le dashboard pour voir les déclencheurs les plus fréquents.

### 1.4 MVP (Version 1) :

- Authentification simple
- Saisie manuelle des déclencheurs et réactions
- Calendrier avec visualisation journalière
- Dashboard avec des analyses graphiques

## 2. Spécifications fonctionnelles

### 2.1. Fonctionnalités principales

**Authentification :**
- Création de compte utilisateur avec mot de passe chiffré.
- Authentification via JSON Web Tokens (JWT).
- Gestion des sessions côté API FastAPI.

![connexion](https://github.com/user-attachments/assets/929fa822-4274-447e-8dcb-f3882a2ad0fd)

**Gestion des déclencheurs et réactions :**
- Déclencheurs et réactions par défaut proposés à la première connexion pour simplifier le démarrage.
- Listes personnalisables pour chaque utilisateur (ajout, modification, suppression).

![admin](https://github.com/user-attachments/assets/2aea54cc-e594-4d67-befc-1fac7641a180)

**Saisie quotidienne :**
- Sélection des déclencheurs du jour.
- Sélection des réactions aux déclencheurs et leur intensité (1 à 5).
- Modification des observations

![nvl obs](https://github.com/user-attachments/assets/d4a7578d-8a1c-4144-be8d-93bcb52c22a5)

**Visualisation des données :**
- Calendrier interactif avec affichage visuel des données.
- Détail de chaque journée accessible.
- Page Analytics :
    - Fréquencedes déclencheurs.
    - Répartition et intensité des réactions.
    - Évolution temporelle.
    - Ajout d'un lien Web PowerBI pour avoir des visualisations interactives disponibles.
 
![calendrier](https://github.com/user-attachments/assets/35260215-b299-457d-981d-24d842e149ee)

**Recherche intelligente :**
- Interface simple type barre de recherche + filtres.

![search](https://github.com/user-attachments/assets/241a5002-23e3-4ccf-8d60-f3d9a427ad7c)

**Gestion du compte :**
- Possibilité de modifier (nom d'utilisateur, mot de passe) ou supprimer le compte.

![compte](https://github.com/user-attachments/assets/de6145c7-e7bd-453c-835f-cc6a63844f1d)

### 2.2. Contraintes fonctionnelles

- Application gratuite à concevoir et à utiliser.
- Données sécurisées et accessibles uniquement à l’utilisateur.
- Interface simplifiée, intuitive.

## 3. Spécifications techniques

### 3.1. Technologies choisies (V1)

**Backend :**
- Langage : Python.
- Framework : FastAPI pour gérer les API REST.
- Base de données : SQLite (locale, légère, adaptée aux petits volumes de données).
- Authentification : JWT.
- ORM : SQLAlchemy.

**Frontend :**
- Streamlit pour une interface utilisateur interactive.

**Infrastructure :**
- Exécution locale via Streamlit.

**Analyse de données :**
- Graphiques Plotly/Matplotlib pour visualisations des données.

**Sécurité :**
- Gestion des secrets et variables d’environnement avec des fichiers .env.
- Bandit pour la sécurité du code Python dans GitHub Actions.
- Trivy pour scanner les vulnérabilités des conteneurs dans GitHub Actions.
- Pytest pour les tests des routes.

## 4. Interface utilisateur

### 4.1. Page d’accueil

- Formulaire de connexion et d’inscription.

### 4.2. Page de gestion des déclencheurs

- Liste des déclencheurs existants.
- Ajout / modification / suppression d'un nouveau déclencheur.
- Utilisation possible d’émojis pour illustrer.

### 4.3. Page de saisie quotidienne

- Calendrier interactif.
- Sélection des déclencheurs du jour.
- Sélection des réactions (avec intensité).

### 4.4. Page analytics

**Graphiques générés avec Plotly :**
- Histogramme des déclencheurs (par intensité).
- Diagramme circulaire des réactions (répartition).
- Graphique linéaire des tendances temporelles.
- Jauge (%) de réactivité mensuelle.

**Recherche avancée :**
- champ de recherche textuelle,
- filtres temporels (plages de dates),
- filtres par réaction/déclencheur/intensité.

## 5. Étapes détaillées de mise en place

### 5.1. Préparation

**Installation des outils :**
- Python, pip, et modules nécessaires : fastapi, uvicorn, sqlalchemy, streamlit, etc.
- Docker
- GitHub Actions
- Trivy

**Planification BDD :**
- Utilisateurs
- Déclencheurs
- Saisies journalières
- Réactions émotionnelles.

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
    - DailyEntry : données journalières (date, intensité, réactions, utilisateur lié).
    - Reaction : réaction du chien au déclencheur.
- Initialiser la base et inclure des déclencheurs par défaut.

**Sécurisation des API :**
- Ajouter des tokens JWT pour gérer les sessions utilisateurs.

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
- Connexion à FastAPI via requêtes HTTP.
- Stockage local du JWT pour les appels sécurisés.

### 5.4. Analyse des données

- Publication de graphiques avec Matplotlib / Plotly.
- Export PDF des données.

### 5.5. Automatisation DevOps

**Conteneurisation :**
- Écrire un Dockerfile pour le backend et l’interface Streamlit.
- Construire et tester l’image localement.

**Pipeline CI/CD :**
- Configurer GitHub Actions pour :
    - Lancer des tests unitaires (FastAPI).

## 6. Application V2

### 6.1. Automatisation DevOps

- Utilisation de Terraform pour automatiser la création et la gestion des ressources cloud sur Oracle Cloud.
- Provisionnement automatisé :
    - Déploiement de machines virtuelles ou services managés.
    - Création des ressources réseau nécessaires (VPC, Load Balancer, etc.).
    - Configuration du cluster K3s pour l’orchestration des conteneurs.
- Intégration de Vault pour la gestion centralisée et sécurisée des secrets (API keys, tokens JWT, identifiants DB…).
- GitHub Actions : pipelines CI/CD pour automatiser le déploiement avant mise en production.

### 6.2. Déploiement cloud

- Déploiement sur Oracle Cloud ou Raspberry Pi.
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

### 6.4 Recherche intelligente

- Elasticsearch pour la recherche (via Docker).

## 7. Maintenance et évolutions futures

**Surveillance continue :**
- Analyse des logs applicatifs et système.
- Mise en place d’un système de rotation et d’archivage des logs.

**Améliorations possibles :**
- Compatible PC et smartphone
- Ajouter des notifications (ex. : rappel de saisie quotidienne).
- Étendre l’analyse avec des graphiques supplémentaires.
- Ajouter une page Médicaments (rappel, liste de médicaments, dosage).
- Ajouter une page suivi des déplacements : carte sur laquelle l'utilisateur signale le début et la fin d'une balade, afin d'évaluer si la distance ou la durée de la balade augmente ou diminue.
