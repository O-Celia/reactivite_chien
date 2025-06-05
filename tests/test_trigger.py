import pytest
import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

@pytest.fixture(scope="module")
def basic_client():
    return TestClient(app)


@pytest.fixture(scope="module")
def user_data():
    uid = uuid.uuid4().hex[:6]
    return {
        "username": f"testuser_{uid}",
        "password": "testpassword",
        "email": f"test_{uid}@example.com"
    }


@pytest.fixture(scope="module")
def auth_client(user_data):
    # Création de l'utilisateur
    response = client.post("/users/", json=user_data)
    if response.status_code not in (200, 201):
        raise Exception(f"User creation failed: {response.status_code} - {response.json()}")
    created_user = response.json()
    user_id = created_user.get("id")
    if not user_id:
        raise Exception("Pas d'id utilisateur retourné à la création")
    # Connexion pour obtenir le token
    login_response = client.post("/users/login", json=user_data)
    if login_response.status_code != 200:
        raise Exception("Échec de la récupération du token. Vérifie les identifiants.")
    token = login_response.json().get("access_token")
    if not token:
        raise Exception("Pas de token reçu.")
    # Mise à jour des headers
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client, user_id
    # Teardown : suppression de l'utilisateur
    client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})


@pytest.fixture
def created_trigger(auth_client):
    client, user_id = auth_client
    data = {"name": "soleil", "user_id": user_id}
    response = client.post("/triggers/", json=data)
    assert response.status_code in (200, 201), f"Erreur à la création du trigger : {response.status_code} - {response.text}"
    trigger = response.json()
    yield trigger
    # Teardown : suppression du trigger créé
    delete_response = client.delete(f"/triggers/{trigger['id']}")
    if delete_response.status_code not in (200, 204):
        print(f"{RED}⚠️ Échec de la suppression du trigger : {delete_response.status_code} - {delete_response.text}{RESET}")
        

# --- Tests ---

def test_create_trigger_pass(auth_client):
    client, user_id = auth_client
    response = client.post("/triggers/", json={"name": "Trigger Test", "user_id": user_id})
    try:
        assert response.status_code in (200, 201)
        print(f"{GREEN}Test passant : création de trigger OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : création de trigger a échoué{RESET}")
        raise
    finally:
        if response.status_code in (200, 201):
            trigger_id = response.json()["id"]
            client.delete(f"/triggers/{trigger_id}")

def test_create_trigger_fail_missing_name(auth_client):
    client, user_id = auth_client
    response = client.post("/triggers/", json={"user_id": user_id})
    try:
        assert response.status_code == 422
        print(f"{GREEN}Test non passant : création de trigger sans nom refusé OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : création de trigger sans nom n’a pas renvoyé 422 mais {response.status_code}{RESET}")
        raise

def test_get_user_triggers_pass(auth_client, created_trigger):
    client, _ = auth_client
    response = client.get("/triggers/")
    try:
        assert response.status_code == 200
        triggers = response.json()
        assert any(t["id"] == created_trigger["id"] for t in triggers)
        print(f"{GREEN}Test passant : récupération de triggers OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : récupération de triggers a échoué{RESET}")
        raise

def test_get_user_triggers_fail_unauthenticated(basic_client):
    response = basic_client.get("/triggers/")
    try:
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"
        print(f"{GREEN}Test non passant : récupération de triggers sans authentification refusé OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : récupération de triggers sans authentification n’a pas renvoyé 401 ou message attendu{RESET}")
        raise

def test_get_trigger_by_id_pass(auth_client, created_trigger):
    client, _ = auth_client
    trigger_id = created_trigger["id"]
    response = client.get(f"/triggers/{trigger_id}")
    try:
        assert response.status_code == 200
        assert response.json()["id"] == trigger_id
        print(f"{GREEN}Test passant : récupération trigger par ID OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : récupération trigger par ID a échoué{RESET}")
        raise

def test_get_trigger_by_id_fail_not_found(auth_client):
    client, _ = auth_client
    response = client.get("/triggers/99999999")
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant : récupération trigger avec ID inexistant échoué OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : récupération trigger avec ID inexistant n’a pas échoué (status {response.status_code}){RESET}")
        raise

def test_update_trigger_pass(auth_client, created_trigger):
    client, _ = auth_client
    trigger_id = created_trigger["id"]
    response = client.put(f"/triggers/{trigger_id}", json={"name": "Trigger modifié"})
    try:
        assert response.status_code == 200
        assert response.json()["name"] == "Trigger modifié"
        print(f"{GREEN}Test passant : mise à jour trigger OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : mise à jour trigger a échoué{RESET}")
        raise

def test_update_trigger_fail_not_found(auth_client):
    client, _ = auth_client
    response = client.put("/triggers/99999999", json={"name": "Trigger modifié"})
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant : mise à jour trigger ID inexistant échoué OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : mise à jour trigger ID inexistant n’a pas échoué (status {response.status_code}){RESET}")
        raise

def test_delete_trigger_pass(auth_client):
    client, user_id = auth_client
    response = client.post("/triggers/", json={"name": "Trigger à supprimer", "user_id": user_id})
    trigger_id = response.json()["id"]
    response = client.delete(f"/triggers/{trigger_id}")
    try:
        assert response.status_code in (200, 204)
        print(f"{GREEN}Test passant : suppression trigger OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : suppression trigger a échoué (status {response.status_code}){RESET}")
        raise

def test_delete_trigger_fail_not_found(auth_client):
    client, _ = auth_client
    response = client.delete("/triggers/99999999")
    try:
        assert response.status_code == 404
        print(f"{GREEN}Test non passant : suppression trigger ID inexistant échoué OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR : suppression trigger ID inexistant n’a pas échoué (status {response.status_code}){RESET}")
        raise

