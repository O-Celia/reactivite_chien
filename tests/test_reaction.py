import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# --------- FIXTURES ------------
@pytest.fixture
def created_reaction():
    """Crée une réaction avant un test et la supprime après."""
    response = client.post("/reactions/", json={
        "name": "Test Réaction"
    })
    reaction = response.json()
    yield reaction
    client.delete(f"/reactions/{reaction['id']}")

# Test Passant : Créer une réaction avec des données valides
def test_create_reaction_pass():
    response = client.post("/reactions/", json={
        "name": "Réaction Test"
    })
    try:
        assert response.status_code in [200, 201]
        print(f"{GREEN}Test passant : création de réaction OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: création de réaction a échoué{RESET}")
        raise
    finally:
        if response.status_code in [200, 201]:
            reaction_id = response.json().get("id")
            client.delete(f"/reactions/{reaction_id}")

# Test Non Passant : Créer une réaction avec un champ manquant
def test_create_reaction_missing_field():
    response = client.post("/reactions/", json={
        # "name" manquant
    })
    try:
        assert response.status_code == 422
        print(f"{GREEN}Test non passant (manque champ obligatoire) : OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: champ obligatoire manquant mais pas d'erreur retournée{RESET}")
        raise

# Test Non Passant : Essayer de récupérer une réaction inexistante
def test_get_nonexistent_reaction():
    response = client.get("/reactions/99999")
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant (GET sur une ID inexistante) : OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: attendu 404 sur ID inexistant, reçu {response.status_code}{RESET}")
        raise

# Test Passant : Lire une réaction existante
def test_get_reaction_pass(created_reaction):
    reaction_id = created_reaction["id"]

    response = client.get(f"/reactions/{reaction_id}")
    try:
        assert response.status_code == 200
        print(f"{GREEN}Test passant : lecture d'une réaction OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: lecture de réaction a échoué{RESET}")
        raise

# Test Passant : Supprimer une réaction existante
def test_delete_reaction_pass():
    response = client.post("/reactions/", json={
        "name": "Réaction Test à supprimer"
    })
    reaction_id = response.json()["id"]

    delete_response = client.delete(f"/reactions/{reaction_id}")
    try:
        assert delete_response.status_code == 200
        print(f"{GREEN}Test passant : suppression d'une réaction OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: suppression de réaction a échoué{RESET}")
        raise

# Test Passant : Mettre à jour une réaction existante
def test_update_reaction_pass(created_reaction):
    reaction_id = created_reaction["id"]

    updated_data = {
        "name": "Réaction mise à jour"
    }

    response = client.put(f"/reactions/{reaction_id}", json=updated_data)
    
    try:
        assert response.status_code == 200
        updated_reaction = response.json()
        assert updated_reaction["name"] == "Réaction mise à jour"
        print(f"{GREEN}Test passant : mise à jour d'une réaction OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: mise à jour de réaction a échoué{RESET}")
        raise
    
# Test Non Passant : Essayer de mettre à jour une réaction inexistante
def test_update_nonexistent_reaction():
    fake_reaction_id = 99999  # ID supposé inexistant

    updated_data = {
        "name": "Réaction inexistante"
    }

    response = client.put(f"/reactions/{fake_reaction_id}", json=updated_data)

    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant : mise à jour sur réaction inexistante renvoie 404 OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: attendu 404 sur update de réaction inexistante, reçu {response.status_code}{RESET}")
        raise
