from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...schemas import UserCreate, UserOut
from ...core.database import get_db
from ...models.user import User

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="username already exists")
    u = User(username=payload.username)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@router.get("/", response_model=List[UserOut])
def list_users(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(User).limit(limit).all()

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="user not found")
    return u
