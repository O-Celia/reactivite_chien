# Tests de l'API FastAPI

Ce répertoire contient les tests unitaires et d'intégration pour l'application FastAPI, centrés sur les endpoints suivants :

- `/entry/` : Gestion des entrées (journaux)
- `/reactions/` : Gestion des réactions
- `/triggers/` : Gestion des déclencheurs
- `/users/` : Gestion des utilisateurs

## Structure

- `test_entry.py` : Vérifie les opérations CRUD sur les entrées.
- `test_reaction.py` : Vérifie les opérations CRUD sur les réactions.
- `test_trigger.py` : Vérifie les opérations CRUD sur les déclencheurs.
- `test_user.py` : Vérifie les opérations CRUD sur les utilisateurs.

Chaque fichier de test suit la structure suivante :
- **Fixtures** : Création et suppression d’objets avant/après les tests.
- **Tests passants** : Cas normaux où les requêtes sont bien formées.
- **Tests non passants** : Vérifie les comportements attendus en cas d'erreurs (ex. champs manquants, ID inexistant).

Les tests utilisent la librairie `pytest` et `fastapi.testclient.TestClient`.

## Lancer les tests

Les tests seront lancés avec :
```bash
pytest tests/ --capture=no
```

## Exemples de tests

### Test réussi

```bash
Test passant : création d'entrée OK
```

### Test échoué

```bash
ERREUR: attendu 404 sur update d'entrée inexistante, reçu 200
```

## Objectif des tests

- Vérifier que les endpoints répondent avec les bons codes HTTP.
- S'assurer que les données sont bien enregistrées, lues, modifiées et supprimées.
- Gérer proprement les cas d’erreur ou les requêtes incomplètes.