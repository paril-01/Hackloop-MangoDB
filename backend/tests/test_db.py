from backend.app.core.database import init_db, SessionLocal
from backend.app.models.activity import Activity


def test_init_db_and_create_activity():
    # Ensure tables exist
    init_db()
    db = SessionLocal()
    try:
        a = Activity(activity_type="unittest", confidence=0.1)
        db.add(a)
        db.commit()
        assert a.id is not None
    finally:
        db.close()
