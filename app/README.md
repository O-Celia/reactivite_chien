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
    ├── entry.py
    ├── reaction.py
    ├── trigger.py
    └── user.py
```

## Configuration de la base de données – database.py

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

### crud/entry.py

- create_daily_entry : crée une entrée journalière avec triggers et réactions associés
- get_daily_entries : récupère toutes les entrées
- get_daily_entry_by_id : récupère une entrée spécifique
- update_daily_entry : met à jour une entrée
- delete_daily_entry : supprime une entrée

### crud/reaction.py

Fonctions standard : create, read, update, delete pour Reaction

### crud/trigger.py

Fonctions standard : create, read, update, delete pour Trigger

### crud/user.py

Fonctions standard : create, read, update, delete pour User
- Ajout d’un getter par username (en attendant que l'authentification des utilisateurs soit ajoutée)

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

Les données sont stockées dans un fichier SQLite :
```bash
/data/db.sqlite3
