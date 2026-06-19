from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_template():
    r = client.post("/api/v1/templates", json={
        "name": "python-ci",
        "language": "Python",
        "stages": ["lint", "test", "build"],
        "triggers": ["push", "pull_request"]
    })
    assert r.status_code == 200
    assert r.json()["status"] == "created"

