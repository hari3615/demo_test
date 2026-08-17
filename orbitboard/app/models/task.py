from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.db import Base
from app.models.label import task_label_association

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="TODO")
    
    project_id = Column(Integer, ForeignKey("projects.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    estimate_days = Column(Float, default=0.0)
    started_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks_assigned")
    comments = relationship("Comment", back_populates="task")
    attachments = relationship("Attachment", back_populates="task")
    labels = relationship("Label", secondary=task_label_association, back_populates="tasks")
