import pytest
import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

@pytest.fixture(scope="module")
def user_data():
    uid = uuid.uuid4().hex[:6]
    return {
        "username": f"reaction_user_{uid}",
        "password": "reactionpass",
        "email": f"reaction_{uid}@example.com"
    }
    
@pytest.fixture(scope="module")
def basic_client():
    return TestClient(app)

@pytest.fixture(scope="module")
def auth_client(user_data):
    # Création de l'utilisateur
    response = client.post("/users/", json=user_data)
    if response.status_code not in (200, 201):
        raise Exception("Échec de création utilisateur")
    user_id = response.json()["id"]

    # Connexion pour obtenir le token
    login = client.post("/users/login", json=user_data)
    if login.status_code != 200:
        raise Exception("Échec de login")
    token = login.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client, user_id

    # Teardown : suppression utilisateur
    client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})


@pytest.fixture
def created_reaction(auth_client):
    client, user_id = auth_client
    data = {"name": "test_reaction", "user_id": user_id}
    response = client.post("/reactions/", json=data)
    assert response.status_code in (200, 201)
    reaction = response.json()
    yield reaction
    # Teardown
    client.delete(f"/reactions/{reaction['id']}")


# --- TESTS ---

def test_create_reaction(auth_client):
    client, user_id = auth_client
    response = client.post("/reactions/", json={"name": "joy", "user_id": user_id})
    try:
        assert response.status_code in (200, 201)
        print(f"{GREEN}Création de réaction OK{RESET}")
    except AssertionError:
        print(f"{RED}Création de réaction a échoué ({response.status_code}){RESET}")
        raise
    finally:
        if response.status_code in (200, 201):
            client.delete(f"/reactions/{response.json()['id']}")

def test_get_user_reactions(auth_client, created_reaction):
    client, _ = auth_client
    response = client.get("/reactions/")
    try:
        assert response.status_code == 200
        assert any(r["id"] == created_reaction["id"] for r in response.json())
        print(f"{GREEN}Récupération des réactions utilisateur OK{RESET}")
    except AssertionError:
        print(f"{RED}Échec de la récupération des réactions utilisateur{RESET}")
        raise

def test_get_reaction_by_id(auth_client, created_reaction):
    client, _ = auth_client
    reaction_id = created_reaction["id"]
    response = client.get(f"/reactions/{reaction_id}")
    try:
        assert response.status_code == 200
        assert response.json()["id"] == reaction_id
        print(f"{GREEN}Récupération d'une réaction par ID OK{RESET}")
    except AssertionError:
        print(f"{RED}Récupération d'une réaction par ID a échoué{RESET}")
        raise

def test_update_reaction(auth_client, created_reaction):
    client, _ = auth_client
    reaction_id = created_reaction["id"]
    response = client.put(f"/reactions/{reaction_id}", json={"name": "updated_reaction"})
    try:
        assert response.status_code == 200
        assert response.json()["name"] == "updated_reaction"
        print(f"{GREEN}Mise à jour de la réaction OK{RESET}")
    except AssertionError:
        print(f"{RED}Échec de la mise à jour de la réaction{RESET}")
        raise

def test_delete_reaction(auth_client):
    client, user_id = auth_client
    # Créer une réaction à supprimer
    response = client.post("/reactions/", json={"name": "to_delete", "user_id": user_id})
    assert response.status_code in (200, 201)
    reaction_id = response.json()["id"]
    # Supprimer
    delete = client.delete(f"/reactions/{reaction_id}")
    try:
        assert delete.status_code in (200, 204)
        print(f"{GREEN}Suppression de la réaction OK{RESET}")
    except AssertionError:
        print(f"{RED}Échec de suppression de la réaction{RESET}")
        raise

def test_get_reaction_not_found(auth_client):
    client, _ = auth_client
    response = client.get("/reactions/999999")
    try:
        assert response.status_code == 404
        print(f"{GREEN}Récupération d'une réaction avec ID inexistant a échoué OK{RESET}")
    except AssertionError:
        print(f"{RED}Récupération d'une réaction avec ID inexistant n'a pas échoué 404{RESET}")
        raise

def test_create_reaction_fail_missing_name(auth_client):
    client, user_id = auth_client
    response = client.post("/reactions/", json={"user_id": user_id})
    try:
        assert response.status_code == 422
        print(f"{GREEN}Test non passant : création de réaction sans nom refusé OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : création de réaction sans nom n’a pas renvoyé 422 mais {response.status_code}{RESET}")
        raise

def test_get_user_reactions_fail_unauthenticated(basic_client):
    response = basic_client.get("/reactions/")
    try:
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"
        print(f"{GREEN}Test non passant : récupération de réactions sans authentification refusé OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : récupération de réactions sans authentification n’a pas renvoyé 401 ou message attendu{RESET}")
        raise

def test_update_reaction_fail_not_found(auth_client):
    client, _ = auth_client
    response = client.put("/reactions/99999999", json={"name": "Réaction modifiée"})
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant : mise à jour réaction ID inexistant échoué OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : mise à jour réaction ID inexistant n’a pas échoué (status {response.status_code}){RESET}")
        raise

def test_delete_reaction_fail_not_found(auth_client):
    client, _ = auth_client
    response = client.delete("/reactions/99999999")
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant : suppression réaction ID inexistant échoué OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : suppression réaction ID inexistant n’a pas échoué (status {response.status_code}){RESET}")
        raise
