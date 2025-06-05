import uuid
import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# ---------------------------------------
#            FIXTURES UTILES
# ---------------------------------------

@pytest.fixture
def user_data():
    uid = uuid.uuid4().hex[:6]
    return {
        "username": f"testuser_{uid}",
        "password": "testpassword",
        "email": f"test_{uid}@example.com"
    }

@pytest.fixture
def created_user(user_data):
    response = client.post("/users/", json=user_data)
    if response.status_code not in (200, 201):
        raise Exception(f"User creation failed: {response.status_code} - {response.json()}")
    user = response.json()
    yield user
    # Teardown
    login_response = client.post("/users/login", json=user_data)
    if login_response.status_code == 200:
        token = login_response.json().get("access_token")
        if token:
            client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})
        else:
            print("⚠️ Pas de token lors du teardown")
    else:
        print(f"⚠️ Échec du login lors du teardown, utilisateur non supprimé")

@pytest.fixture
def created_user_no_teardown(user_data):
    response = client.post("/users/", json=user_data)
    return response.json()

# ---------------------------------------
#         TESTS PASSANTS
# ---------------------------------------

def test_create_user_pass(user_data):
    response = client.post("/users/", json=user_data)
    try:
        assert response.status_code in [200, 201]
        print(f"{GREEN}Test passant : création d'utilisateur OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: création d'utilisateur a échoué{RESET}")
        raise
    finally:
        if response.status_code in [200, 201]:
            token = client.post("/users/login", json=user_data).json()["access_token"]
            client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})


def test_login_user_pass(created_user, user_data):
    response = client.post("/users/login", json=user_data)
    try:
        assert response.status_code == 200
        assert "access_token" in response.json()
        print(f"{GREEN}Test passant : connexion utilisateur OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: connexion utilisateur a échoué{RESET}")
        raise


def test_get_me_pass(created_user, user_data):
    token = client.post("/users/login", json=user_data).json()["access_token"]
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    try:
        assert response.status_code == 200
        assert response.json()["username"] == created_user["username"]
        print(f"{GREEN}Test passant : lecture de /me OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: lecture de /me a échoué{RESET}")
        raise


def test_update_me_pass(created_user, user_data):
    token = client.post("/users/login", json=user_data).json()["access_token"]
    update_data = {"email": "updated@example.com"}
    response = client.put("/users/me", json=update_data, headers={"Authorization": f"Bearer {token}"})
    try:
        assert response.status_code == 200
        assert response.json()["email"] == "updated@example.com"
        print(f"{GREEN}Test passant : mise à jour de /me OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: mise à jour de /me a échoué{RESET}")
        raise


def test_delete_me_pass(created_user_no_teardown, user_data):
    token = client.post("/users/login", json=user_data).json()["access_token"]
    response = client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})
    try:
        assert response.status_code == 200
        print(f"{GREEN}Test passant : suppression de /me OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: suppression de /me a échoué{RESET}")
        raise


def test_create_user_success_without_email():
    uid = uuid.uuid4().hex[:6]
    response = client.post("/users/", json={
        "username": f"testuser_{uid}",
        "password": "strongpassword"
    })
    try:
        assert response.status_code in [200, 201]
        print(f"{GREEN}Test passant : création sans email OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: création sans email a échoué{RESET}")
        raise
    finally:
        if response.status_code in [200, 201]:
            token = client.post("/users/login", json={
                "username": f"testuser_{uid}",
                "password": "strongpassword"
            }).json().get("access_token")
            if token:
                client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})


# ---------------------------------------
#         TESTS NON PASSANTS
# ---------------------------------------

def test_create_user_fail_missing_username():
    response = client.post("/users/", json={
        "email": "testuser@example.com",
        "password": "strongpassword"
    })
    try:
        assert response.status_code == 422
        print(f"{GREEN}Test non passant : échec attendu si username manquant{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: création sans username n'a pas échoué{RESET}")
        raise


def test_create_user_fail_missing_password():
    uid = uuid.uuid4().hex[:6]
    response = client.post("/users/", json={
        "username": f"testuser_{uid}",
        "email": "testuser@example.com"
    })
    try:
        assert response.status_code == 422
        print(f"{GREEN}Test non passant : échec attendu si password manquant{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: création sans password n'a pas échoué{RESET}")
        raise


def test_login_user_fail_wrong_password(created_user, user_data):
    bad_login = {
        "username": user_data["username"],
        "password": "wrongpassword"
    }
    response = client.post("/users/login", json=bad_login)
    try:
        assert response.status_code >= 400
        print(f"{GREEN}Test non passant : connexion avec mauvais mot de passe rejetée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: connexion avec mauvais mot de passe acceptée{RESET}")
        raise


def test_get_me_fail_unauthenticated():
    response = client.get("/users/me")
    try:
        assert response.status_code == 401
        print(f"{GREEN}Test non passant : accès à /me sans authentification rejeté OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: accès à /me sans authentification accepté{RESET}")
        raise


def test_update_me_fail_no_token():
    update_data = {"email": "fail@example.com"}
    response = client.put("/users/me", json=update_data)
    try:
        assert response.status_code == 401
        print(f"{GREEN}Test non passant : mise à jour sans token rejetée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: mise à jour sans token acceptée{RESET}")
        raise


def test_delete_me_fail_unauthenticated():
    response = client.delete("/users/me")
    try:
        assert response.status_code == 401
        print(f"{GREEN}Test non passant : suppression sans authentification rejetée OK{RESET}")
    except AssertionError:
        print(f"{RED}ERREUR: suppression sans authentification acceptée{RESET}")
        raise
