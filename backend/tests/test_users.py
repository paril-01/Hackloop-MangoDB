from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_create_and_get_user():
    payload = {"username": "tester123"}
    r = client.post("/api/users/", json=payload)
    if r.status_code == 200:
        body = r.json()
        assert body["username"] == "tester123"

        uid = body["id"]
        r2 = client.get(f"/api/users/{uid}")
        assert r2.status_code == 200
        assert r2.json()["username"] == "tester123"
    else:
        # If user already exists, ensure it's present in the list
        assert r.status_code == 400
        rlist = client.get('/api/users/')
        assert rlist.status_code == 200
        users = rlist.json()
        assert any(u['username'] == 'tester123' for u in users)
