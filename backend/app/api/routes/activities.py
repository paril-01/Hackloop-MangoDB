from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ...schemas import ActivityCreate, ActivityOut
from ...core.database import get_db
from ...models.activity import Activity
from ...core.security import get_current_user


router = APIRouter(prefix="/api/activities", tags=["activities"])

@router.post("/", response_model=ActivityOut)
def create_activity(payload: ActivityCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    uid = payload.user_id or (current_user.id if current_user else None)
    activity = Activity(
        user_id=uid,
        activity_type=payload.activity_type,
        confidence=payload.confidence,
        details=payload.details,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

@router.get("/", response_model=List[ActivityOut])
def list_activities(limit: int = 50, db: Session = Depends(get_db)):
    items = db.query(Activity).order_by(Activity.timestamp.desc()).limit(limit).all()
    return items
