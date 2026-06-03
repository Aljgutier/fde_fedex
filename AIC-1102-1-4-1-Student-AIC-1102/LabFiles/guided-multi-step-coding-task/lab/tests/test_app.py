import sys
import os
import pytest

# Ensure project root is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, store


@pytest.fixture
def client():
    store._tasks.clear()
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
