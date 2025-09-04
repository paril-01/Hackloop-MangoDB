import time
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.session_cleanup import session_cleanup
from backend.app.core.config import settings
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.session import Session as SessionModel
from datetime import datetime, timedelta, timezone

client = TestClient(app)


def test_background_cleanup_removes_expired_sessions():
    # set a short cleanup interval for the test
    session_cleanup.interval = 1

    username = 'bg_user'
    pw = 'bgpw'

    db = SessionLocal()
    db.query(User).filter(User.username == username).delete()
    db.commit()
    db.close()

    # create a session by logging in
    r = client.post('/api/auth/login', json={'username': username, 'password': pw})
    assert r.status_code == 200
    token = client.cookies.get('replika_session')
    assert token is not None

    # mark the session expired
    db = SessionLocal()
    s = db.query(SessionModel).filter(SessionModel.token == token).first()
    assert s is not None
    s.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    db.add(s)
    db.commit()
    db.close()

    # start cleanup task explicitly in test (TestClient may not have started lifecycle hooks)
    import asyncio
    loop = asyncio.get_event_loop()
    session_cleanup.start(loop)
    # wait for the background task to run
    time.sleep(2)
    # stop task
    loop.run_until_complete(session_cleanup.stop())

    db = SessionLocal()
    s2 = db.query(SessionModel).filter(SessionModel.token == token).first()
    db.close()
    assert s2 is None
