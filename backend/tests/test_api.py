import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_create_and_list_activity():
    payload = {"activity_type": "testing", "confidence": 0.5}
    r = client.post("/api/activities/", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["activity_type"] == "testing" or body["activity_type"] == "testing"

    r2 = client.get("/api/activities/")
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)
