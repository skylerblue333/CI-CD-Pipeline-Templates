from fastapi.testclient import TestClient
from src.main import app, templates

client = TestClient(app)


def setup_function():
    templates.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_get_list_and_delete_template():
    payload = {
        "name": "python-ci",
        "language": "Python",
        "stages": ["lint", "test", "build"],
        "triggers": ["push", "pull_request"],
    }
    created = client.post("/api/v1/templates", json=payload)
    assert created.status_code == 201
    assert client.get("/api/v1/templates/python-ci").json()["language"] == "Python"
    assert len(client.get("/api/v1/templates").json()) == 1
    assert client.delete("/api/v1/templates/python-ci").status_code == 204
    assert client.get("/api/v1/templates/python-ci").status_code == 404


def test_duplicate_template_returns_conflict():
    payload = {"name": "go-ci", "language": "Go", "stages": ["test"], "triggers": ["push"]}
    assert client.post("/api/v1/templates", json=payload).status_code == 201
    assert client.post("/api/v1/templates", json=payload).status_code == 409


def test_invalid_template_is_rejected():
    payload = {"name": "", "language": "Python", "stages": [], "triggers": []}
    assert client.post("/api/v1/templates", json=payload).status_code == 422
