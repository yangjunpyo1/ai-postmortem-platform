from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from app.database import get_db
from app.models.incident import Incident
from app.schemas.incident import IncidentResponse
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/incidents", tags=["similar"])

@router.get("/{incident_id}/similar", response_model=List[IncidentResponse])
def get_similar_incidents(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 현재 장애 조회
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        return []

    # 카테고리 기반 + 키워드 기반 검색 (현재 장애 제외)
    similar = db.query(Incident).filter(
        Incident.id != incident_id,
        or_(
            Incident.category == incident.category,
            Incident.severity == incident.severity
        )
    ).order_by(Incident.created_at.desc()).limit(5).all()

    return similar