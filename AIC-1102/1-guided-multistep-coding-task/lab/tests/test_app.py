import sys
import os
from itertools import count
import pytest

# Ensure project root is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, store


@pytest.fixture
def client():
    store._tasks.clear()
    store._ids = count(1)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task_returns_201_with_task(client):
    response = client.post("/tasks", json={"title": "Write docs"})
    assert response.status_code == 201
    body = response.get_json()
    assert body["title"] == "Write docs"
    assert body["status"] == "pending"
    assert "id" in body


def test_create_task_with_invalid_title_missing(client):
    response = client.post("/tasks", json={"status": "pending"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "title is required"}


def test_create_task_with_invalid_title_empty(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400
    assert response.get_json() == {"error": "title must be a non-empty string"}


def test_create_task_with_invalid_title_type(client):
    response = client.post("/tasks", json={"title": 123})
    assert response.status_code == 400
    assert response.get_json() == {"error": "title must be a non-empty string"}


def test_create_task_with_invalid_status(client):
    response = client.post("/tasks", json={"title": "Ship feature", "status": "blocked"})
    assert response.status_code == 422
    assert response.get_json() == {
        "error": "status must be one of: pending, in_progress, done",
        "valid_statuses": ["pending", "in_progress", "done"],
    }


def test_get_task_returns_200_when_found(client):
    created = client.post("/tasks", json={"title": "Write tests"}).get_json()
    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.get_json() == created


def test_get_task_returns_404_when_missing(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "task not found"}


def test_update_task_title_only(client):
    created = client.post("/tasks", json={"title": "Old title"}).get_json()

    response = client.put(f"/tasks/{created['id']}", json={"title": "New title"})
    assert response.status_code == 200
    updated = response.get_json()
    assert updated["title"] == "New title"
    assert updated["status"] == "pending"


def test_update_task_status_only(client):
    created = client.post("/tasks", json={"title": "Start work"}).get_json()

    response = client.put(f"/tasks/{created['id']}", json={"status": "in_progress"})
    assert response.status_code == 200
    updated = response.get_json()
    assert updated["title"] == "Start work"
    assert updated["status"] == "in_progress"


def test_update_task_title_and_status(client):
    created = client.post("/tasks", json={"title": "Draft"}).get_json()

    response = client.put(
        f"/tasks/{created['id']}",
        json={"title": "Final", "status": "done"},
    )
    assert response.status_code == 200
    assert response.get_json() == {"id": created["id"], "title": "Final", "status": "done"}


def test_update_task_returns_404_when_missing(client):
    response = client.put("/tasks/999", json={"title": "Nope"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "task not found"}


def test_update_task_invalid_title(client):
    created = client.post("/tasks", json={"title": "Keep"}).get_json()

    response = client.put(f"/tasks/{created['id']}", json={"title": ""})
    assert response.status_code == 400
    assert response.get_json() == {"error": "title must be a non-empty string"}


def test_update_task_invalid_status(client):
    created = client.post("/tasks", json={"title": "Keep"}).get_json()

    response = client.put(f"/tasks/{created['id']}", json={"status": "blocked"})
    assert response.status_code == 422
    assert response.get_json() == {
        "error": "status must be one of: pending, in_progress, done",
        "valid_statuses": ["pending", "in_progress", "done"],
    }


def test_update_task_with_empty_payload(client):
    created = client.post("/tasks", json={"title": "Keep"}).get_json()

    response = client.put(f"/tasks/{created['id']}", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "at least one of title or status is required"}


def test_delete_task_returns_204_and_removes_task(client):
    created = client.post("/tasks", json={"title": "Delete me"}).get_json()

    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204
    assert response.get_data() == b""

    get_response = client.get(f"/tasks/{created['id']}")
    assert get_response.status_code == 404


def test_delete_task_returns_404_when_missing(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "task not found"}


def test_list_tasks_with_status_filter(client):
    client.post("/tasks", json={"title": "A", "status": "pending"})
    client.post("/tasks", json={"title": "B", "status": "done"})
    client.post("/tasks", json={"title": "C", "status": "done"})

    response = client.get("/tasks?status=done")
    assert response.status_code == 200
    body = response.get_json()
    assert len(body) == 2
    assert {task["title"] for task in body} == {"B", "C"}
    assert {task["status"] for task in body} == {"done"}


def test_list_tasks_without_status_filter_returns_all(client):
    client.post("/tasks", json={"title": "A", "status": "pending"})
    client.post("/tasks", json={"title": "B", "status": "in_progress"})

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_list_tasks_with_unknown_status_returns_empty(client):
    client.post("/tasks", json={"title": "A", "status": "pending"})

    response = client.get("/tasks?status=unknown")
    assert response.status_code == 200
    assert response.get_json() == []
