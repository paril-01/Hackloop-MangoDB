from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..core.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    activity_type = Column(String(128), index=True, nullable=False)
    confidence = Column(Float, nullable=False, default=0.0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(String(1024), nullable=True)
