"""Simple seed script to create an initial user and sample activity."""
from app.core.database import init_db, SessionLocal
from app.models.user import User
from app.models.activity import Activity


def seed():
    """Idempotent seed: creates demo user and a sample activity if missing."""
    init_db()
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == 'demo').first()
        if not user:
            user = User(username='demo')
            db.add(user)
            db.commit()
            db.refresh(user)

        # create a sample activity if none exist for demo user
        exists = db.query(Activity).filter(Activity.user_id == user.id).first()
        if not exists:
            a = Activity(user_id=user.id, activity_type="demo_activity", confidence=0.99, details="seeded")
            db.add(a)
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
