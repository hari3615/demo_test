from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db import Base
import datetime


class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    target_url = Column(String, nullable=False)
    event_type = Column(String, nullable=False)  # e.g. "task.created", "task.updated"
    secret = Column(String, nullable=True)  # HMAC signing secret
    enabled = Column(Boolean, default=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_triggered_at = Column(DateTime, nullable=True)
    failure_count = Column(Integer, default=0)
