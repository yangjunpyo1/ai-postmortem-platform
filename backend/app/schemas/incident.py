from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncidentCreate(BaseModel):
    title: str
    severity: str
    category: str
    started_at: datetime

class IncidentResponse(BaseModel):
    id: int
    user_id: int
    title: str
    severity: str
    category: str
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    downtime: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IncidentUpdate(BaseModel):
    status: Optional[str] = None
    ended_at: Optional[datetime] = None