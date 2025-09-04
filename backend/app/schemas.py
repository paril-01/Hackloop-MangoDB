from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Health(BaseModel):
    status: str = "ok"

class UserCreate(BaseModel):
    username: str = Field(..., max_length=128)
    password: Optional[str] = Field(None, min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class ActivityCreate(BaseModel):
    user_id: Optional[int]
    activity_type: str
    confidence: float
    details: Optional[str] = None


class LoginPayload(BaseModel):
    username: str
    password: str

class ActivityOut(BaseModel):
    id: int
    user_id: Optional[int]
    activity_type: str
    confidence: float
    timestamp: Optional[datetime]
    details: Optional[str]

    class Config:
        orm_mode = True

class AutomationCreate(BaseModel):
    name: str
    script: str
    description: Optional[str] = None

class AutomationOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    script: str
    created_at: Optional[datetime]
    last_run_at: Optional[datetime]

    class Config:
        orm_mode = True
