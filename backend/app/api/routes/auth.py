from fastapi import APIRouter, Response, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import uuid4
from ...core.database import get_db
from ...models.user import User
from ...models.session import Session as SessionModel
from ...schemas import LoginPayload, UserCreate
from ...core import security as core_security
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from ...core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix='/api/auth', tags=['auth'])


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.post('/login')
def login(payload: LoginPayload, response: Response, db: Session = Depends(get_db)):
    """Password-based login. Creates user if missing. Enforces simple lockout on repeated failures."""
    username = payload.username
    password = payload.password
    if not username or not password:
        raise HTTPException(status_code=400, detail='username and password required')

    user = db.query(User).filter(User.username == username).first()
    if not user:
        # create user with hashed password
        user = User(username=username, password_hash=hash_password(password))
        db.add(user)
        db.commit()
        db.refresh(user)

    # check lockout (use timezone-aware UTC datetimes)
    now = datetime.now(timezone.utc)
    if user.locked_until:
        lu = user.locked_until
        # coerce naive timestamps to UTC for backward compatibility
        if lu.tzinfo is None:
            from datetime import timezone as _tz
            lu = lu.replace(tzinfo=_tz.utc)
        if lu > now:
            raise HTTPException(status_code=403, detail='account locked, try later')

    if not user.password_hash or not verify_password(password, user.password_hash):
        # increment failed attempts
        user.failed_attempts = (user.failed_attempts or 0) + 1
        # lock after 5 attempts for 15 minutes
        if user.failed_attempts >= 5:
            user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
            user.failed_attempts = 0
        db.add(user)
        db.commit()
        raise HTTPException(status_code=401, detail='invalid credentials')

    # reset failed attempts on success
    user.failed_attempts = 0
    user.locked_until = None
    db.add(user)
    db.commit()

    token = str(uuid4())
    s = SessionModel(token=token, user_id=user.id)
    # set expiry
    s.expires_at = datetime.now(timezone.utc) + timedelta(seconds=getattr(settings, 'SESSION_TTL_SECONDS', 3600))
    db.add(s)
    db.commit()

    # set cookie
    response.set_cookie('replika_session', token, httponly=True, samesite='lax')
    return {'status': 'ok'}


@router.post('/logout')
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    # remove cookie and session on server (best effort)
    token = request.cookies.get('replika_session')
    if token:
        s = db.query(SessionModel).filter(SessionModel.token == token).first()
        if s:
            db.delete(s)
            db.commit()
    response.delete_cookie('replika_session')
    return {'status': 'ok'}


@router.get('/me')
def me(current_user=Depends(core_security.get_current_user)):
    if not current_user:
        return {"user": None}
    return {"user": {"id": current_user.id, "username": current_user.username}}
