from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.incident import Incident
from app.schemas.statistics import StatisticsResponse
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/statistics", tags=["statistics"])

@router.get("", response_model=StatisticsResponse)
def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Incident).count()

    severity_counts = db.query(
        Incident.severity, func.count(Incident.id)
    ).group_by(Incident.severity).all()
    by_severity = {s: c for s, c in severity_counts}

    category_counts = db.query(
        Incident.category, func.count(Incident.id)
    ).group_by(Incident.category).all()
    by_category = {c: cnt for c, cnt in category_counts}

    avg_downtime = db.query(func.avg(Incident.downtime)).scalar()

    return StatisticsResponse(
        total_incidents=total,
        by_severity=by_severity,
        by_category=by_category,
        average_downtime=avg_downtime
    )