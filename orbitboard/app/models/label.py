from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db import Base

task_label_association = Table(
    "task_label_association",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String)

    tasks = relationship("Task", secondary=task_label_association, back_populates="labels")
