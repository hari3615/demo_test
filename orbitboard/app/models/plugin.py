from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db import Base
import datetime


class Plugin(Base):
    __tablename__ = "plugins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # The module path that will be dynamically imported, e.g. "orbitboard.plugins.slack"
    module_path = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)
    config_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
