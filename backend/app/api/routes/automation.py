from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...schemas import AutomationCreate, AutomationOut
from ...core.database import get_db
from ...models.automation import AutomationMacro

router = APIRouter(prefix="/api/automation", tags=["automation"])

@router.post("/", response_model=AutomationOut)
def create_macro(payload: AutomationCreate, db: Session = Depends(get_db)):
    macro = AutomationMacro(name=payload.name, script=payload.script, description=payload.description)
    db.add(macro)
    db.commit()
    db.refresh(macro)
    return macro

@router.get("/")
def list_macros(db: Session = Depends(get_db)):
    return db.query(AutomationMacro).all()
