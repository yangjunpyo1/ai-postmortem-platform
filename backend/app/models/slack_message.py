from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class SlackMessage(Base):
    __tablename__ = "slack_messages"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    user_name = Column(String(255), nullable=False)
    message = Column(String(4000), nullable=False)
    timestamp = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())

    incident = relationship("Incident", back_populates="slack_messages")