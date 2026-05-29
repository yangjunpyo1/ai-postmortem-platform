from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Postmortem(Base):
    __tablename__ = "postmortems"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    summary = Column(Text, nullable=True)
    timeline = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    resolution = Column(Text, nullable=True)
    prevention = Column(Text, nullable=True)
    affected_range = Column(Text, nullable=True)
    assignee = Column(String(255), nullable=True)
    similar_incidents = Column(Text, nullable=True)
    is_ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    incident = relationship("Incident", back_populates="postmortem")