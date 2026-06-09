import pytest

from backend.app import create_app
from backend.store import store


@pytest.fixture
def client():
    store._users.clear()
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_create_user_returns_201(client):
    response = client.post("/api/users", json={"username": "ada", "email": "ada@example.com"})
    assert response.status_code == 201
    body = response.get_json()
    assert body["username"] == "ada"


def test_create_user_missing_fields_returns_400(client):
    response = client.post("/api/users", json={"username": "ada"})
    assert response.status_code == 400


def test_get_user_returns_user(client):
    created = client.post(
        "/api/users", json={"username": "ada", "email": "ada@example.com"}
    ).get_json()
    response = client.get(f"/api/users/{created['id']}")
    assert response.status_code == 200
    assert response.get_json()["username"] == "ada"


def test_get_user_not_found(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404
