# data/

Ce dossier contient les scripts nécessaires à la gestion de la base de données SQLite utilisée dans le projet.

## Contenu

### `01_create_table.py`
Ce script initialise la base de données `db.sqlite3` en créant les tables suivantes :
- `users` : informations des utilisateurs.
- `daily_entries` : entrées journalières de réactions.
- `triggers` : éléments déclencheurs.
- `reactions` : types de réactions observées.
- Tables d'association `daily_entry_triggers` et `daily_entry_reactions` : relations N-N entre entrées et déclencheurs/réactions.

Les relations entre les tables sont gérées avec des clés étrangères, avec suppression en cascade (`ON DELETE CASCADE`).

### `02_insert_test_data.py`
Ce script insère des données de test pour faciliter le développement et l’expérimentation :
- Utilisateurs fictifs (`obelix`, `tintin`)
- Liste de déclencheurs (`vélo`, `chien`, `enfant`...)
- Réactions possibles (`aboiement`, `fuite`, `grognement`...)
- Quelques entrées journalières avec leurs déclencheurs et réactions associées.

### `03_delete_data.py`
Permet de supprimer proprement toutes les données des tables (y compris les séquences d’autoincrémentation), utile pour les réinitialisations ou tests répétés.

---

## Utilisation

1. Lancer `01_create_table.py` pour créer les tables.
2. Lancer `02_insert_test_data.py` pour remplir la base avec des exemples.
3. (Optionnel) Lancer `03_delete_data.py` pour nettoyer la base.

---

## Base de données

- **Type** : SQLite
- **Fichier généré** : `db.sqlite3`
- **Relations** : Modélisation relationnelle avec associations entre entrées, déclencheurs et réactions.

---

## Objectif

Ce module met en place une base de données simple et relationnelle pour démontrer la structuration d’un backend léger, utilisable avec FastAPI ou tout autre framework Python.


