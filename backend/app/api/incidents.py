from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.database import get_db
from app.models.incident import Incident
from app.models.postmortem import Postmortem
from app.models.slack_message import SlackMessage
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

@router.get("", response_model=List[IncidentResponse])
def get_incidents(
    severity: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Incident)
    if severity:
        query = query.filter(Incident.severity == severity)
    if category:
        query = query.filter(Incident.category == category)
    if status:
        query = query.filter(Incident.status == status)
    
    page_size = 10
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all()

@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="장애를 찾을 수 없습니다.")
    return incident

@router.post("", response_model=IncidentResponse)
def create_incident(
    incident_data: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = Incident(
        user_id=current_user.id,
        title=incident_data.title,
        severity=incident_data.severity,
        category=incident_data.category,
        started_at=incident_data.started_at,
        status="발생중"
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

@router.patch("/{incident_id}/resolve", response_model=IncidentResponse)
def resolve_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="장애를 찾을 수 없습니다.")

    ended_at = datetime.utcnow()
    downtime = (ended_at - incident.started_at).total_seconds() / 60

    incident.status = "종료"
    incident.ended_at = ended_at
    incident.downtime = downtime
    db.commit()
    db.refresh(incident)
    return incident

@router.delete("/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="장애를 찾을 수 없습니다.")

    db.query(SlackMessage).filter(SlackMessage.incident_id == incident_id).delete()
    db.query(Postmortem).filter(Postmortem.incident_id == incident_id).delete()
    db.delete(incident)
    db.commit()
    return {"message": "삭제되었습니다."}