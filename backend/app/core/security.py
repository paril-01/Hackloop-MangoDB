from fastapi import Request, HTTPException, Depends
from typing import Optional
from .database import get_db
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.session import Session as SessionModel
from datetime import datetime, timezone


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    token = request.cookies.get('replika_session')
    if not token:
        return None
    s = db.query(SessionModel).filter(SessionModel.token == token).first()
    if not s:
        return None
    # check expiry
    if s.expires_at:
        expires = s.expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if expires < datetime.now(timezone.utc):
            # session expired: remove it and treat as unauthenticated
            try:
                db.delete(s)
                db.commit()
            except Exception:
                pass
            return None
    user = db.query(User).filter(User.id == s.user_id).first()
    if not user:
        return None
    return user
