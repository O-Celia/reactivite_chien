import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# --------- FIXTURES ------------
@pytest.fixture
def created_user():
    """Crée un utilisateur avant un test et le supprime après."""
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "testuser@example.com"
    })
    user = response.json()
    yield user
    client.delete(f"/users/{user['id']}")

# Test Passant : Créer un utilisateur avec des données valides
def test_create_user_pass():
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "testuser@example.com"
    })
    try:
        assert response.status_code in [200, 201]
        print(f"{GREEN}Test passant : création d'utilisateur OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: création d'utilisateur a échoué{RESET}")
        raise
    finally:
        if response.status_code in [200, 201]:
            user_id = response.json().get("id")
            client.delete(f"/users/{user_id}")

# Test Non Passant : Créer un utilisateur avec un champ manquant
def test_create_user_missing_field():
    response = client.post("/users/", json={
        # "username" manquant
        "email": "missinguser@example.com"
    })
    try:
        assert response.status_code == 422
        print(f"{GREEN}Test non passant (champ manquant) : OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: champ obligatoire manquant mais pas d'erreur retournée{RESET}")
        raise

# Test Non Passant : Essayer de récupérer un utilisateur inexistant
def test_get_nonexistent_user():
    response = client.get("/users/99999")
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant (GET sur un ID inexistant) : OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: attendu 404 sur ID inexistant, reçu {response.status_code}{RESET}")
        raise

# Test Passant : Lire un utilisateur existant
def test_get_user_pass(created_user):
    user_id = created_user["id"]

    response = client.get(f"/users/{user_id}")
    try:
        assert response.status_code == 200
        print(f"{GREEN}Test passant : lecture d'un utilisateur OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: lecture d'utilisateur a échoué{RESET}")
        raise

# Test Passant : Supprimer un utilisateur existant
def test_delete_user_pass():
    response = client.post("/users/", json={
        "username": "user_to_delete",
        "email": "user_to_delete@example.com"
    })
    user_id = response.json()["id"]

    delete_response = client.delete(f"/users/{user_id}")
    try:
        assert delete_response.status_code == 200
        print(f"{GREEN}Test passant : suppression d'un utilisateur OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: suppression d'utilisateur a échoué{RESET}")
        raise

# Test Passant : Mettre à jour un utilisateur existant
def test_update_user_pass(created_user):
    user_id = created_user["id"]

    updated_data = {
        "username": "updated_user",
        "email": "updated_user@example.com"
    }

    response = client.put(f"/users/{user_id}", json=updated_data)
    
    try:
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["username"] == "updated_user"
        print(f"{GREEN}Test passant : mise à jour d'un utilisateur OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: mise à jour d'utilisateur a échoué{RESET}")
        raise

# Test Non Passant : Essayer de mettre à jour un utilisateur inexistant
def test_update_nonexistent_user():
    fake_user_id = 99999  # ID supposé inexistant

    updated_data = {
        "username": "nonexistent_user",
        "email": "nonexistent_user@example.com"
    }

    response = client.put(f"/users/{fake_user_id}", json=updated_data)

    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant : mise à jour sur utilisateur inexistant renvoie 404 OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: attendu 404 sur update d'utilisateur inexistant, reçu {response.status_code}{RESET}")
        raise
