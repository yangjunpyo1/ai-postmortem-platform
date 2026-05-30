from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostmortemResponse(BaseModel):
    id: int
    incident_id: int
    summary: Optional[str] = None
    timeline: Optional[str] = None
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    prevention: Optional[str] = None
    affected_range: Optional[str] = None
    assignee: Optional[str] = None
    similar_incidents: Optional[str] = None
    is_ai_generated: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PostmortemUpdate(BaseModel):
    summary: Optional[str] = None
    timeline: Optional[str] = None
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    prevention: Optional[str] = None
    affected_range: Optional[str] = None
    assignee: Optional[str] = None