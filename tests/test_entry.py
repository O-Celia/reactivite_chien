import pytest
import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# ---------- FIXTURES ----------

@pytest.fixture(scope="module")
def user_data():
    uid = uuid.uuid4().hex[:6]
    return {
        "username": f"entry_user_{uid}",
        "password": "entrypass",
        "email": f"entry_{uid}@example.com"
    }

@pytest.fixture(scope="module")
def auth_client(user_data):
    # Créer l'utilisateur
    response = client.post("/users/", json=user_data)
    assert response.status_code in (200, 201)
    user_id = response.json()["id"]

    # Connexion pour récupérer le token
    login = client.post("/users/login", json=user_data)
    assert login.status_code == 200
    token = login.json()["access_token"]

    # Authentifier le client
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client, user_id

    # Supprimer l'utilisateur
    client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})


@pytest.fixture
def created_entry(auth_client):
    client, user_id = auth_client
    data = {
        "entry_date": "2024-04-26",
        "severity": 5,
        "comment": "Entrée pour tests",
        "triggers": [],
        "reactions": [],
        "user_id": user_id
    }
    response = client.post("/entry/", json=data)
    entry = response.json()
    yield entry
    if "id" in entry:
        client.delete(f"/entry/{entry['id']}")


# ---------- TESTS ----------

def test_create_entry_pass(auth_client):
    client, user_id = auth_client
    data = {
        "entry_date": "2024-04-26",
        "severity": 5,
        "comment": "Test commentaire valide",
        "triggers": [],
        "reactions": [],
        "user_id": user_id
    }
    response = client.post("/entry/", json=data)
    try:
        assert response.status_code in [200, 201]
        print(f"{GREEN}Test passant : création d'entrée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: création d'entrée a échoué{RESET}")
        raise
    finally:
        if response.status_code in [200, 201]:
            entry_id = response.json()["id"]
            client.delete(f"/entry/{entry_id}")


def test_create_entry_missing_field(auth_client):
    client, user_id = auth_client
    data = {
        "severity": 5,
        "comment": "Commentaire sans date",
        "triggers": [],
        "reactions": [],
        "user_id": user_id
    }
    response = client.post("/entry/", json=data)
    try:
        assert response.status_code == 422
        print(f"{GREEN}Test non passant (champ manquant) : OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: champ manquant mais pas d'erreur retournée{RESET}")
        raise


def test_get_nonexistent_entry(auth_client):
    client, _ = auth_client
    response = client.get("/entry/999999")
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant (GET ID inexistant) : OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: attendu 404, reçu {response.status_code}{RESET}")
        raise


def test_get_entry_pass(auth_client, created_entry):
    client, _ = auth_client
    entry_id = created_entry["id"]
    response = client.get(f"/entry/{entry_id}")
    try:
        assert response.status_code == 200
        print(f"{GREEN}Test passant : lecture d'une entrée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: lecture d'entrée a échoué{RESET}")
        raise


def test_delete_entry_pass(auth_client):
    client, user_id = auth_client
    data = {
        "entry_date": "2024-04-26",
        "severity": 5,
        "comment": "Suppression test",
        "triggers": [],
        "reactions": [],
        "user_id": user_id
    }
    response = client.post("/entry/", json=data)
    entry_id = response.json()["id"]

    delete_response = client.delete(f"/entry/{entry_id}")
    try:
        assert delete_response.status_code == 200
        print(f"{GREEN}Test passant : suppression d'une entrée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: suppression d'entrée a échoué{RESET}")
        raise


def test_update_entry_pass(auth_client, created_entry):
    client, user_id = auth_client
    entry_id = created_entry["id"]
    updated_data = {
        "entry_date": "2024-04-27",
        "severity": 3,
        "comment": "Commentaire mis à jour",
        "triggers": ["chien"],
        "reactions": ["aboiement"],
        "user_id": user_id
    }
    response = client.put(f"/entry/{entry_id}", json=updated_data)
    try:
        assert response.status_code == 200
        updated = response.json()
        assert updated["entry_date"] == "2024-04-27"
        assert updated["severity"] == 3
        assert updated["comment"] == "Commentaire mis à jour"
        assert updated["triggers"] == ["chien"]
        assert updated["reactions"] == ["aboiement"]
        print(f"{GREEN}Test passant : mise à jour entrée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: mise à jour d'entrée a échoué{RESET}")
        raise


def test_update_nonexistent_entry(auth_client):
    client, user_id = auth_client
    updated_data = {
        "entry_date": "2024-04-27",
        "severity": 4,
        "comment": "MAJ entrée inexistante",
        "triggers": ["chien"],
        "reactions": ["aboiement"],
        "user_id": user_id
    }
    response = client.put("/entry/999999", json=updated_data)
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant : mise à jour inexistante 404 OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: attendu 404 sur update inexistante, reçu {response.status_code}{RESET}")
        raise


def test_delete_nonexistent_entry(auth_client):
    client, _ = auth_client
    response = client.delete("/entry/999999")
    try:
        assert response.status_code == 404
        print(f"{GREEN}Suppression entrée inexistante : OK{RESET}")
    except AssertionError:
        print(f"{RED}Suppression entrée inexistante devrait retourner 404{RESET}")
        raise


def test_get_entry_without_auth(created_entry):
    unauth_client = TestClient(app)
    response = unauth_client.get(f"/entry/{created_entry['id']}")
    try:
        assert response.status_code == 401
        print(f"{GREEN}Lecture sans authentification : refusée (401) OK{RESET}")
    except AssertionError:
        print(f"{RED}Accès sans authentification non refusé{RESET}")
        raise
