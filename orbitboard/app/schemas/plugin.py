from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PluginBase(BaseModel):
    name: str
    module_path: str
    enabled: bool = True
    config_json: Optional[str] = None


class PluginCreate(PluginBase):
    pass


class PluginRun(BaseModel):
    plugin_name: str
    payload: Optional[dict] = {}


class Plugin(PluginBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
