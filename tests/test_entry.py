import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# --------- FIXTURES ------------
@pytest.fixture
def created_entry():
    """Crée une entrée avant un test et la supprime après."""
    response = client.post("/entry/", json={
        "user_id": 1000,
        "entry_date": "2024-04-26",
        "severity": 5,
        "comment": "Entrée pour tests",
        "triggers": [],
        "reactions": []
    })
    entry = response.json()
    yield entry
    client.delete(f"/entry/{entry['id']}")


# --------- TESTS ------------

# Test Passant : Créer une entrée avec un user_id valide
def test_create_entry_pass():
    response = client.post("/entry/", json={
        "user_id": 1000,
        "entry_date": "2024-04-26",
        "severity": 5,
        "comment": "Test commentaire valide",
        "triggers": [],
        "reactions": []
    })
    try:
        assert response.status_code in [200, 201]
        print(f"{GREEN}Test passant : création d'entrée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: création d'entrée a échoué{RESET}")
        raise
    finally:
        if response.status_code in [200, 201]:
            entry_id = response.json().get("id")
            client.delete(f"/entry/{entry_id}")


# Test Non Passant : Créer une entrée sans entry_date
def test_create_entry_missing_field():
    response = client.post("/entry/", json={
        "user_id": 1000,
        # "entry_date" manquant
        "severity": 5,
        "comment": "Commentaire sans date",
        "triggers": [],
        "reactions": []
    })
    try:
        assert response.status_code == 422
        print(f"{GREEN}Test non passant (manque champ obligatoire) : OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: champ obligatoire manquant mais pas d'erreur retournée{RESET}")
        raise


# Test Non Passant : Essayer de récupérer une entrée inexistante
def test_get_nonexistent_entry():
    response = client.get("/entry/99999")
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant (GET sur un ID inexistant) : OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: attendu 404 sur ID inexistant, reçu {response.status_code}{RESET}")
        raise


# Test Passant : Lire une entrée existante
def test_get_entry_pass(created_entry):
    entry_id = created_entry["id"]

    response = client.get(f"/entry/{entry_id}")
    try:
        assert response.status_code == 200
        print(f"{GREEN}Test passant : lecture d'une entrée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: lecture d'entrée a échoué{RESET}")
        raise

# Test Passant : Supprimer une entrée existante
def test_delete_entry_pass():
    # On crée une entrée temporaire pour ce test
    response = client.post("/entry/", json={
        "user_id": 1000,
        "entry_date": "2024-04-26",
        "severity": 5,
        "comment": "Test suppression",
        "triggers": [],
        "reactions": []
    })
    entry_id = response.json()["id"]

    delete_response = client.delete(f"/entry/{entry_id}")
    try:
        assert delete_response.status_code == 200
        print(f"{GREEN}Test passant : suppression d'une entrée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: suppression d'entrée a échoué{RESET}")
        raise

# Test Passant : Mettre à jour une entrée existante
def test_update_entry_pass(created_entry):
    entry_id = created_entry["id"]

    updated_data = {
        "user_id": 1000,
        "entry_date": "2024-04-27",
        "severity": 3,
        "comment": "Commentaire mis à jour",
        "triggers": [1],
        "reactions": [3]
    }

    response = client.put(f"/entry/{entry_id}", json=updated_data)
    
    try:
        assert response.status_code == 200
        updated_entry = response.json()
        assert updated_entry["entry_date"] == "2024-04-27"
        assert updated_entry["severity"] == 3
        assert updated_entry["comment"] == "Commentaire mis à jour"
        assert updated_entry["triggers"] == ['bruit']
        assert updated_entry["reactions"] == ['fuite']
        print(f"{GREEN}Test passant : mise à jour d'une entrée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: mise à jour d'entrée a échoué{RESET}")
        raise
    
# Test Non Passant : Essayer de mettre à jour une entrée inexistante
def test_update_nonexistent_entry():
    fake_entry_id = 99999  # ID supposé inexistant

    updated_data = {
        "user_id": 1000,
        "entry_date": "2024-04-27",
        "severity": 4,
        "comment": "Tentative de mise à jour sur une entrée inexistante",
        "triggers": [2],
        "reactions": [2]
    }

    response = client.put(f"/entry/{fake_entry_id}", json=updated_data)

    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant : mise à jour sur entrée inexistante renvoie 404 OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: attendu 404 sur update d'entrée inexistante, reçu {response.status_code}{RESET}")
        raise

