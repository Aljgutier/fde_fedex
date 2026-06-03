import pytest

from tickets.app import create_app
from tickets.store import store


@pytest.fixture
def client():
    store._tickets.clear()
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_tickets_empty(client):
    response = client.get("/tickets")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_ticket_returns_201_with_timestamps(client):
    response = client.post(
        "/tickets",
        json={"title": "Login fails", "description": "500 on submit"},
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body["title"] == "Login fails"
    assert body["status"] == "open"
    assert body["created_at"] == body["updated_at"]


def test_create_ticket_missing_title_returns_400(client):
    response = client.post("/tickets", json={"description": "no title"})
    assert response.status_code == 400


def test_get_ticket_returns_ticket(client):
    created = client.post(
        "/tickets", json={"title": "t", "description": "d"}
    ).get_json()
    response = client.get(f"/tickets/{created['id']}")
    assert response.status_code == 200
    assert response.get_json()["id"] == created["id"]


def test_get_ticket_not_found_returns_404(client):
    response = client.get("/tickets/999")
    assert response.status_code == 404


def test_patch_status_success_returns_updated_ticket(client):
    created = client.post(
        "/tickets", json={"title": "t", "description": "d"}
    ).get_json()
    response = client.patch(
        f"/tickets/{created['id']}/status", json={"status": "in_progress"}
    )
    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "in_progress"
    assert body["updated_at"] >= created["updated_at"]


def test_patch_status_not_found_returns_404(client):
    response = client.patch("/tickets/999/status", json={"status": "open"})
    assert response.status_code == 404


def test_patch_status_missing_body_returns_400(client):
    created = client.post(
        "/tickets", json={"title": "t", "description": "d"}
    ).get_json()
    response = client.patch(f"/tickets/{created['id']}/status")
    assert response.status_code == 400


def test_patch_status_missing_field_returns_400(client):
    created = client.post(
        "/tickets", json={"title": "t", "description": "d"}
    ).get_json()
    response = client.patch(f"/tickets/{created['id']}/status", json={})
    assert response.status_code == 400


def test_patch_status_invalid_value_returns_400(client):
    created = client.post(
        "/tickets", json={"title": "t", "description": "d"}
    ).get_json()
    response = client.patch(
        f"/tickets/{created['id']}/status", json={"status": "banana"}
    )
    assert response.status_code == 400


def test_patch_status_allows_any_valid_transition(client):
    created = client.post(
        "/tickets", json={"title": "t", "description": "d"}
    ).get_json()
    for target in ("in_progress", "resolved", "open", "closed"):
        response = client.patch(
            f"/tickets/{created['id']}/status", json={"status": target}
        )
        assert response.status_code == 200
        assert response.get_json()["status"] == target
