import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# --------- FIXTURES ------------
@pytest.fixture
def created_trigger():
    """Crée un trigger avant un test et le supprime après."""
    response = client.post("/triggers/", json={
        "name": "Test Trigger"
    })
    trigger = response.json()
    yield trigger
    client.delete(f"/triggers/{trigger['id']}")

# Test Passant : Créer un trigger avec des données valides
def test_create_trigger_pass():
    response = client.post("/triggers/", json={
        "name": "Trigger Test"
    })
    try:
        assert response.status_code in [200, 201]
        print(f"{GREEN}Test passant : création de trigger OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: création de trigger a échoué{RESET}")
        raise
    finally:
        if response.status_code in [200, 201]:
            trigger_id = response.json().get("id")
            client.delete(f"/triggers/{trigger_id}")

# Test Non Passant : Créer un trigger avec un champ manquant
def test_create_trigger_missing_field():
    response = client.post("/triggers/", json={
        # "name" manquant
    })
    try:
        assert response.status_code == 422
        print(f"{GREEN}Test non passant (manque champ obligatoire) : OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: champ obligatoire manquant mais pas d'erreur retournée{RESET}")
        raise

# Test Non Passant : Essayer de récupérer un trigger inexistant
def test_get_nonexistent_trigger():
    response = client.get("/triggers/99999")
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant (GET sur une ID inexistante) : OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: attendu 404 sur ID inexistant, reçu {response.status_code}{RESET}")
        raise

# Test Passant : Lire un trigger existant
def test_get_trigger_pass(created_trigger):
    trigger_id = created_trigger["id"]

    response = client.get(f"/triggers/{trigger_id}")
    try:
        assert response.status_code == 200
        print(f"{GREEN}Test passant : lecture d'un trigger OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: lecture de trigger a échoué{RESET}")
        raise

# Test Passant : Supprimer un trigger existant
def test_delete_trigger_pass():
    response = client.post("/triggers/", json={
        "name": "Trigger Test à supprimer"
    })
    trigger_id = response.json()["id"]

    delete_response = client.delete(f"/triggers/{trigger_id}")
    try:
        assert delete_response.status_code == 200
        print(f"{GREEN}Test passant : suppression d'un trigger OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: suppression de trigger a échoué{RESET}")
        raise

# Test Passant : Mettre à jour un trigger existant
def test_update_trigger_pass(created_trigger):
    trigger_id = created_trigger["id"]

    updated_data = {
        "name": "Trigger mis à jour"
    }

    response = client.put(f"/triggers/{trigger_id}", json=updated_data)
    
    try:
        assert response.status_code == 200
        updated_trigger = response.json()
        assert updated_trigger["name"] == "Trigger mis à jour"
        print(f"{GREEN}Test passant : mise à jour d'un trigger OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: mise à jour de trigger a échoué{RESET}")
        raise

# Test Non Passant : Essayer de mettre à jour un trigger inexistant
def test_update_nonexistent_trigger():
    fake_trigger_id = 99999  # ID supposé inexistant

    updated_data = {
        "name": "Trigger inexistant"
    }

    response = client.put(f"/triggers/{fake_trigger_id}", json=updated_data)

    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant : mise à jour sur trigger inexistant renvoie 404 OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: attendu 404 sur update de trigger inexistant, reçu {response.status_code}{RESET}")
        raise
