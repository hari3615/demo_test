from datetime import datetime, timezone
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.db import Base

# Association table for tasks and labels (many-to-many)
task_labels = Table(
    "task_labels",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("label_id", Integer, ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True)
)

class ProjectMember(Base):
    """
    Model linking users and projects with custom roles.
    """
    __tablename__ = "project_members"

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role = Column(String(50), default="member", nullable=False)  # 'owner', 'admin', 'member', 'viewer'
    joined_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
