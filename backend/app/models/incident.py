from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    severity = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    status = Column(String(50), default="발생중")
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    downtime = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="incidents")
    postmortem = relationship("Postmortem", back_populates="incident", uselist=False)
    slack_messages = relationship("SlackMessage", back_populates="incident")