from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.postmortem import Postmortem
from app.models.incident import Incident
from app.schemas.postmortem import PostmortemResponse, PostmortemUpdate
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/incidents", tags=["postmortems"])


@router.get("/{incident_id}/postmortem", response_model=PostmortemResponse)
def get_postmortem(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    postmortem = db.query(Postmortem).filter(Postmortem.incident_id == incident_id).first()
    if not postmortem:
        raise HTTPException(status_code=404, detail="Postmortem 문서를 찾을 수 없습니다.")
    return postmortem


@router.post("/{incident_id}/postmortem/generate")
def generate_postmortem(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="장애를 찾을 수 없습니다.")

    # TODO: Lambda(postmortem) 트리거
    # 현재는 빈 Postmortem 생성
    existing = db.query(Postmortem).filter(Postmortem.incident_id == incident_id).first()
    if existing:
        return {"message": "이미 생성된 Postmortem 문서가 있습니다.", "id": existing.id}

    postmortem = Postmortem(
        incident_id=incident_id,
        is_ai_generated=True
    )
    db.add(postmortem)
    db.commit()
    db.refresh(postmortem)
    return {"message": "Postmortem 자동 생성을 시작합니다.", "id": postmortem.id}


@router.put("/{incident_id}/postmortem", response_model=PostmortemResponse)
def update_postmortem(
    incident_id: int,
    update_data: PostmortemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    postmortem = db.query(Postmortem).filter(Postmortem.incident_id == incident_id).first()
    if not postmortem:
        raise HTTPException(status_code=404, detail="Postmortem 문서를 찾을 수 없습니다.")

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(postmortem, field, value)

    db.commit()
    db.refresh(postmortem)
    return postmortem