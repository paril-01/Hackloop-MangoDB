from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.database import SessionLocal
from backend.app.models.user import User

client = TestClient(app)


def test_register_and_login_success():
    username = "authuser"
    password = "password123"

    # ensure fresh start
    db = SessionLocal()
    db.query(User).filter(User.username == username).delete()
    db.commit()
    db.close()

    r = client.post("/api/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200
    # cookie should be set on client
    assert "replika_session" in client.cookies

    # user should exist in DB
    db = SessionLocal()
    u = db.query(User).filter(User.username == username).first()
    assert u is not None
    assert u.username == username
    db.close()


def test_failed_attempts_and_lockout():
    username = "lockuser"
    correct_pw = "pw"

    # ensure fresh user
    db = SessionLocal()
    db.query(User).filter(User.username == username).delete()
    db.commit()
    db.close()

    # create user with correct password
    r = client.post("/api/auth/login", json={"username": username, "password": correct_pw})
    assert r.status_code == 200
    # logout to clear session
    client.post("/api/auth/logout")

    # attempt wrong password 5 times -> each returns 401; after 5th the account should be locked
    for i in range(5):
        r = client.post("/api/auth/login", json={"username": username, "password": "bad"})
        assert r.status_code == 401

    # verify DB lock state
    db = SessionLocal()
    u = db.query(User).filter(User.username == username).first()
    assert u is not None
    assert u.locked_until is not None
    assert u.failed_attempts == 0

    # now even correct password should be rejected (403 locked)
    r = client.post("/api/auth/login", json={"username": username, "password": correct_pw})
    assert r.status_code == 403

    # clear the lock (simulate expiry) and try correct login again
    u.locked_until = None
    u.failed_attempts = 0
    db.add(u)
    db.commit()
    db.close()

    r = client.post("/api/auth/login", json={"username": username, "password": correct_pw})
    assert r.status_code == 200
