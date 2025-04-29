# sql/

Ce dossier contient les scripts SQL destinés à initialiser, peupler et réinitialiser une base de données **MySQL** pour l'application. Ces fichiers sont conservés à des fins de portabilité ou de migration depuis SQLite vers un système de gestion de base de données plus robuste.

## Contenu

### `01_create_table.sql`
Crée toutes les tables nécessaires pour la base de données :
- `users` : utilisateurs de l'application
- `daily_entries` : entrées journalières décrivant les réactions d’un chien
- `triggers` : déclencheurs d’une réaction (stimuli)
- `reactions` : types de réactions observées
- Tables d'association `daily_entry_triggers` et `daily_entry_reactions` pour gérer les relations N-N

Les relations entre les entités sont gérées via des **clés étrangères avec suppression en cascade**.

---

### `02_insert_test_data.sql`
Insère un jeu de **données fictives** dans les différentes tables :
- Deux utilisateurs : `obelix` et `tintin`
- Plusieurs déclencheurs : `vélo`, `chien`, `visiteur`...
- Réactions types : `aboiement`, `fuite`, `grognement`...
- Trois entrées journalières avec des associations aux déclencheurs et aux réactions

Ce jeu de données permet de tester facilement les affichages ou les fonctionnalités liées aux filtres, analyses ou visualisations.

---

### `03_reset_data.sql`
Script de **nettoyage complet** de la base :
- Supprime toutes les données des tables
- Réinitialise les compteurs `AUTO_INCREMENT`

Utile pour repartir de zéro lors des tests ou du développement continu.

---

## Compatibilité

- Compatible avec **MySQL** et **MariaDB**
- Non compatible tel quel avec SQLite (cf. dossier `/data/` pour cela)

---

## Objectif

Permet de préparer une base relationnelle MySQL en cas de passage à un backend plus robuste, ou pour tester l’application dans des contextes de production ou d’hébergement cloud.

---

## Structure générale

- Tables principales : `users`, `daily_entries`, `triggers`, `reactions`
- Tables de liaison : `daily_entry_triggers`, `daily_entry_reactions`
- Relations 1-N et N-N avec contraintes d’intégrité référentielle

