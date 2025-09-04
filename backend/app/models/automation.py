from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from ..core.database import Base

class AutomationMacro(Base):
    __tablename__ = "automation_macros"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, index=True)
    description = Column(String(512), nullable=True)
    script = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_run_at = Column(DateTime(timezone=True), nullable=True)
