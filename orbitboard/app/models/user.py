from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    projects = relationship("Project", back_populates="owner")
    tasks_assigned = relationship("Task", back_populates="assignee")
    comments = relationship("Comment", back_populates="author")
