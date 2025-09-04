import threading
import time
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.session import Session as SessionModel

client = TestClient(app)


def _post_login(username, password, results, idx):
    r = client.post("/api/auth/login", json={"username": username, "password": password})
    results[idx] = r.status_code


def test_simultaneous_failed_attempts_lock_behavior():
    username = "concurrent_user"
    correct_pw = "goodpw"

    # ensure fresh user
    db = SessionLocal()
    db.query(User).filter(User.username == username).delete()
    db.commit()
    db.close()

    # create user by logging in once
    r = client.post("/api/auth/login", json={"username": username, "password": correct_pw})
    assert r.status_code == 200
    client.post("/api/auth/logout")

    # now spawn multiple threads sending bad passwords concurrently
    threads = []
    n = 8
    results = [None] * n
    for i in range(n):
        t = threading.Thread(target=_post_login, args=(username, "wrongpw", results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # All responses should be either 401 (invalid creds) or 403 (locked) depending on timing
    assert all(code in (401, 403) for code in results)

    # confirm there was progress: either locked_until was set or failed_attempts increased
    db = SessionLocal()
    u = db.query(User).filter(User.username == username).first()
    assert u is not None
    assert (u.locked_until is not None) or (u.failed_attempts and u.failed_attempts > 0)
    db.close()


def test_session_expiry_and_server_side_deletion():
    username = "session_user"
    pw = "seshpw"

    # fresh user
    db = SessionLocal()
    db.query(User).filter(User.username == username).delete()
    db.commit()
    db.close()

    # login to create a session
    r = client.post("/api/auth/login", json={"username": username, "password": pw})
    assert r.status_code == 200
    token = client.cookies.get('replika_session')
    assert token is not None

    # verify a server-side session exists
    db = SessionLocal()
    s = db.query(SessionModel).filter(SessionModel.token == token).first()
    assert s is not None

    # delete session server-side (simulate expiry/cleanup)
    db.delete(s)
    db.commit()
    db.close()

    # make a request that relies on current user; routes check for get_current_user and should treat as unauthenticated
    r2 = client.get('/api/users/')
    assert r2.status_code == 200
    # the client cookie still exists, but server no longer recognizes it; ensure server didn't crash and responded normally
