from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
from typing import Generator

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    # needed for SQLite in single-threaded apps
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def init_db() -> None:
    """Create tables."""
    # Import all model modules so they are registered on Base.metadata
    # This keeps model definitions colocated but ensures metadata sees them
    try:
        from ..models import user  # noqa: F401
        from ..models import activity  # noqa: F401
        from ..models import automation  # noqa: F401
    except Exception:
        # best-effort import; if models are elsewhere, create_all may still work
        pass

    Base.metadata.create_all(bind=engine)

    # NOTE: schema migrations are handled by Alembic. Remove fallback ALTERs to avoid
    # divergent behavior between dev and CI. Run `alembic upgrade head` during CI/startup.

# Dependency for FastAPI endpoints
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
