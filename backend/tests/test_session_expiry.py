from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.session import Session as SessionModel
from datetime import datetime, timedelta, timezone

client = TestClient(app)


def test_session_auto_expiry_cleanup():
    username = "expiry_user"
    pw = "expirepw"

    db = SessionLocal()
    db.query(User).filter(User.username == username).delete()
    db.commit()
    db.close()

    # login, create session
    r = client.post('/api/auth/login', json={'username': username, 'password': pw})
    assert r.status_code == 200
    token = client.cookies.get('replika_session')
    assert token is not None

    # set session as expired in DB
    db = SessionLocal()
    s = db.query(SessionModel).filter(SessionModel.token == token).first()
    assert s is not None
    s.expires_at = datetime.now(timezone.utc) - timedelta(seconds=10)
    db.add(s)
    db.commit()
    db.close()
    # make a request to an endpoint that depends on get_current_user; that should remove expired session
    r2 = client.post('/api/activities/', json={'activity_type': 'test', 'confidence': 0.1})
    assert r2.status_code == 200

    # server should have removed the session row
    db = SessionLocal()
    s2 = db.query(SessionModel).filter(SessionModel.token == token).first()
    assert s2 is None
    db.close()
