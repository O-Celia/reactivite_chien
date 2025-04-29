# App/ – Backend de l’API

Ce dossier contient la logique principale de l'API FastAPI qui permet de gérer des entrées journalières d’un utilisateur, avec des réactions et déclencheurs associés. Il est structuré de manière modulaire avec des dossiers **crud/**, **models/**, **schemas/**, et **routes/**.

## Arborescence

```bash
app/
│
├── database.py         # Configuration SQLAlchemy et moteur de base de données
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

### entry.py

- create_daily_entry : crée une entrée journalière avec triggers et réactions associés
- get_daily_entries : récupère toutes les entrées
- get_daily_entry_by_id : récupère une entrée spécifique
- update_daily_entry : met à jour une entrée
- delete_daily_entry : supprime une entrée

### reaction.py, trigger.py, user.py

Fonctions standard : create, read, update, delete
**user.py** inclut aussi une fonction pour récupérer un utilisateur par username (en attendant l'ajout de l’authentification).

## Schémas Pydantic – *schemas/*

Permettent de valider et formater les données échangées via l’API.
- DailyEntryBase, DailyEntryCreate, DailyEntryRead, DailyEntryUpdate
- TriggerBase, TriggerCreate, TriggerRead, TriggerUpdate
- ReactionBase, ReactionCreate, ReactionRead, ReactionUpdate
- UserBase, UserCreate, UserRead, UserUpdate

## Utilisation avec FastAPI

Les routes définies dans **routes/** utilisent les fonctions **crud/** pour offrir une API RESTful :
- POST /entry/ : Créer une entrée
- GET /entry/ : Lister les entrées
- GET /entry/{id} : Lire une entrée
- PUT /entry/{id} : Modifier une entrée
- DELETE /entry/{id} : Supprimer une entrée

Même logique pour les routes triggers/, reactions/, users/.

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
