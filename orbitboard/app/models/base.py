from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base

from app.db import Base

class TimestampMixin:
    """
    Mixin to automatically add creation and update timestamps to tables.
    Uses timezone-aware UTC datetime values.
    """
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
