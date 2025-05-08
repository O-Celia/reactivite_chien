# App/ – Backend de l’API

Ce dossier contient la logique principale de l'API FastAPI qui permet de gérer des entrées journalières d’un utilisateur, avec des réactions et déclencheurs associés. Il est structuré de manière modulaire avec des dossiers **crud/**, **models/**, **schemas/**, **utils** et **routes/**.

## Arborescence

```bash
app/
│
├── database.py         # Configuration SQLAlchemy et moteur de base de données
├── init_db.py
├── populate_test_data.py
├── .env.example
├── utils
│   ├── auth.py
│   └── dependencies.py
├── crud/               # Fonctions CRUD (Create, Read, Update, Delete)
│   ├── entry.py
│   ├── reaction.py
│   ├── trigger.py
│   └── user.py
├── models/             # Modèles SQLAlchemy
│   ├── entry.py
│   ├── reaction.py
│   ├── trigger.py
│   └── user.py
├── schemas/            # Schémas Pydantic pour validation et sérialisation
│   ├── entry.py
│   ├── reaction.py
│   ├── trigger.py
│   └── user.py
└── routes/             # Endpoints FastAPI (à intégrer dans l’API principale)
│   ├── entry.py
│   ├── reaction.py
│   ├── trigger.py
│   └── user.py
├── main.py             # Point d'entrée de l'API FastAPI
└── requirements.txt    # Dépendances Python de l'application
```

## Création et remplissage de la base de données - *init_db et populate_test_data*

### init_db.py

Ce script initialise la base de données SQLite à partir des modèles définis dans models/. Il :
- Crée le dossier data/ s’il n’existe pas.
- Supprime toutes les tables existantes (utile en phase de test/développement).
- Recrée toutes les tables via SQLAlchemy.

Utilisation :
```bash
python app/init_db.py
```

## populate_test_data.py

Ce script insère des données de test dans la base :
- Ajoute une série de déclencheurs (Trigger) comme "bruit", "vélo", "chien", etc.
- Ajoute une série de réactions (Reaction) comme "aboiement", "tremblement", etc.

Il se connecte à la base via une session SQLAlchemy et valide les ajouts avec commit().

Utilisation :
```bash
python app/populate_test_data.py
```

## Configuration de la base de données – *database.py*

Utilise **SQLAlchemy** avec une base SQLite locale :

- DATABASE_PATH pointe vers ../data/db.sqlite3
- engine instancie un moteur SQLAlchemy
- SessionLocal permet de créer des sessions
- Base est la base de déclaration des modèles

## Modèles – *models/*

Les modèles décrivent la structure des tables SQL et les relations :

- DailyEntry : Entrée journalière avec date de la création de l'entrée, date de l'incident, sévérité de la réaction, commentaire, utilisateur, déclencheurs et réactions.
- Trigger : Facteurs déclencheurs (many-to-many avec DailyEntry)
- Reaction : Réactions observées (many-to-many avec DailyEntry)
- User : Utilisateur de l'application

Les relations sont gérées avec des tables d’association (entry_trigger, entry_reaction).

## Fonctions CRUD – *crud/*

Ce dossier regroupe les fonctions d’interaction avec la base de données (Create, Read, Update, Delete), utilisées dans les routes FastAPI. Chaque fichier correspond à une entité du modèle, sauf search.py qui est dédié aux requêtes spécifiques.

### entry.py

Le modèle **DailyEntry** représente une entrée quotidienne enregistrée par l'utilisateur, contenant une date, un niveau de sévérité, un commentaire, ainsi que des listes de triggers (déclencheurs) et de reactions (réactions) associées à cette entrée.

Fonctions principales :
- Création d'une entrée quotidienne, avec possible création de déclencheurs ou réactions.
- Mise à jour ou suppression d'une entrée existante.
- Récupération des entrées (toutes ou par ID).
- Recherche avancée par date, sévérité, texte, déclencheurs et réactions.

### reaction.py

Une **Reaction** est la réponse comportementale de l’animal à un déclencheur identifié (ex : "aboiement", "tension sur la laisse", "fuite", etc.).

Fonctions principales :
- Création, mise à jour et suppression d’une réaction.
- Liste des réactions personnalisées ou par défaut.
- Clonage des réactions par défaut vers un utilisateur.

### trigger.py

Un **Trigger** (déclencheur) est un facteur identifié par l'utilisateur comme étant susceptible de provoquer une réaction chez son chien (ex : "vélo", "chien inconnu", etc.).

Fonctions principales :
- Création, mise à jour et suppression d’un déclencheur.
- Liste des déclencheurs personnalisés de l'utilisateur ou par défaut (communs à tous).
- Clonage des déclencheurs par défaut vers un utilisateur.

### user.py

Le modèle **User** représente chaque utilisateur de l'application. Il comprend des informations d'identification (nom d'utilisateur, email, mot de passe hashé) ainsi que des métadonnées telles que first_login.

Fonctions principales :
- Création de compte avec vérification de l'unicité (nom d'utilisateur et email).
- Récupération et mise à jour du profil utilisateur.
- Suppression du compte.
- Mise à jour du statut de première connexion (first_login).

### search.py

Une fonction de recherche avancée permet de filtrer les entrées par :
- Période (start_date, end_date)
- Intensité (severity)
- Contenu du commentaire (query)
- Déclencheurs (triggers)
- Réactions (reactions)

## Schémas Pydantic – *schemas/*

Le projet utilise Pydantic pour valider les données des requêtes et des réponses via des schémas structurés. Voici un aperçu des principaux modèles utilisés :

### User

- UserBase: Champs de base (nom d'utilisateur et e-mail).
- UserCreate: Inclut le mot de passe pour l'inscription.
- UserRead: Représente un utilisateur complet avec id, created_at, et first_login.
- UserUpdate: Champs modifiables.
- LoginData: Données pour l'authentification.
- TokenResponse: Réponse de l'authentification avec un token JWT.

### Daily Entry

- DailyEntryBase: Champs de base communs (entry_date, severity, comment).
- DailyEntryCreate: Ajoute triggers, reactions, user_id pour la création.
- DailyEntryRead: Lecture complète avec id, created_at, user_id, triggers, reactions.
- DailyEntryUpdate: Tous les champs optionnels pour modification.

### Trigger

- TriggerBase: Nom du déclencheur.
- TriggerCreate: Ajoute l’user_id.
- TriggerUpdate: Hérite de TriggerBase.
- TriggerRead: Contient id et user_id.
- CloneRequest: Permet de dupliquer une liste de déclencheurs d’un utilisateur à un autre.

### Reaction

- ReactionBase: Nom de la réaction.
- ReactionCreate: Ajoute l’user_id.
- ReactionUpdate: Hérite de ReactionBase.
- ReactionRead: Contient id et user_id.
- CloneRequest: Permet de dupliquer une liste de réactions.

### Search

- SearchRequest: Requête multi-critères pour filtrer les entrées (query, dates, triggers, reactions, severities).
- SearchResult: Format standardisé des résultats de recherche.

## API Routes - *routes/*

L’API est structurée autour de plusieurs entités principales : Utilisateur, Déclencheur (Trigger), Réaction, Entrée journalière, et Recherche. Les routes suivent les conventions REST avec authentification sur les endpoints sensibles.

### Authentification & Utilisateur

- POST /users/ — Créer un utilisateur.
- POST /users/login — Authentification (renvoie un token).
- GET /users/me — Récupère le profil de l'utilisateur connecté.
- PUT /users/me — Met à jour le profil de l'utilisateur connecté.
- DELETE /users/me — Supprime le compte de l'utilisateur connecté.
- PATCH /users/{user_id} — Mise à jour partielle des identifiants utilisateur (usage interne ou admin).

### Déclencheurs

- POST /triggers/ — Créer un déclencheur.
- GET /triggers/?user_id=... — Lister les déclencheurs d’un utilisateur.
- GET /triggers/default — Lister les déclencheurs par défaut.
- POST /triggers/clone_selected — Cloner des déclencheurs sélectionnés.
- GET /triggers/{trigger_id} — Obtenir un déclencheur par ID.
- PUT /triggers/{trigger_id} — Mettre à jour un déclencheur.
- DELETE /triggers/{trigger_id} — Supprimer un déclencheur.

### Réactions

- POST /reactions/ — Créer une réaction.
- GET /reactions/?user_id=... — Lister les réactions d’un utilisateur.
- GET /reactions/default — Lister les réactions par défaut.
- POST /reactions/clone_selected — Cloner des réactions sélectionnées.
- GET /reactions/{reaction_id} — Obtenir une réaction par ID.
- PUT /reactions/{reaction_id} — Mettre à jour une réaction.
- DELETE /reactions/{reaction_id} — Supprimer une réaction.

### Entrées journalières

- POST /entries/ — Créer une entrée journalière.
- GET /entries/ — Lister les entrées de l’utilisateur connecté.
- PUT /entries/{entry_id} — Mettre à jour une entrée.
- DELETE /entries/{entry_id} — Supprimer une entrée.

### Recherche

- POST /search/ — Recherche avancée sur les entrées (requiert authentification).

## Utilitaires d'authentification et de dépendances - *utils/*

Ce dossier contient des fonctions utilitaires essentielles pour la gestion de l’authentification, des tokens JWT, ainsi que des dépendances utilisées avec FastAPI. Il regroupe deux modules principaux : auth.py et dependencies.py.

### Gestion de l'authentification

Ce module permet de :
- Hasher les mots de passe avec bcrypt via passlib.
- Vérifier les mots de passe lors de la connexion utilisateur.
- Générer des tokens d’accès JWT sécurisés contenant les informations d'identité de l'utilisateur (champ "sub").
- Gérer l’expiration des tokens (par défaut 60 minutes).

Fonctions principales :
- hash_password(password: str) -> str : retourne le hash du mot de passe.
- verify_password(plain_password: str, hashed_password: str) -> bool : vérifie qu’un mot de passe correspond à son hash.
- create_access_token(data: dict, expires_delta: timedelta | None = None) : génère un JWT signé avec une durée d’expiration personnalisable.

### Dépendances FastAPI

Ce module fournit les dépendances utilisées dans les endpoints pour :
- Ouvrir et fermer les connexions à la base de données SQLAlchemy.
- Extraire et valider l’utilisateur courant à partir du token JWT envoyé dans l’en-tête Authorization.

Fonctions principales :
- get_db() : gère une session SQLAlchemy (connexion à la base).
- get_current_user(token: str, db: Session) : décode le token, vérifie sa validité, récupère l'utilisateur en base et le renvoie.

Utilise :
- OAuth2PasswordBearer pour gérer les tokens Bearer.
- jose.jwt pour décoder les tokens.
- HTTPException pour gérer les erreurs d'identification.

## Données

Les données sont stockées localement dans un fichier SQLite :
```bash
/data/db.sqlite3
```

## Initialisation

- main.py : point d’entrée de l’API FastAPI. Il initialise l’application, crée la base de données via SQLAlchemy et monte les routes principales (users, triggers, reactions, entries).
- requirements.txt : contient toutes les dépendances nécessaires à l’exécution de l’application (FastAPI, SQLAlchemy, Streamlit, Plotly, etc.).

## Lancer l'application

**1. Création d'un environnement virtuel**

```bash
python -m venv venv
source venv/bin/activate
```

**2. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**3. Lancer l'API**

```bash
uvicorn main:app --reload
```
