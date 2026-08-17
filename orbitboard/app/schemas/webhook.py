from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WebhookBase(BaseModel):
    name: str
    target_url: str
    event_type: str
    secret: Optional[str] = None
    enabled: bool = True
    project_id: Optional[int] = None


class WebhookCreate(WebhookBase):
    pass


class Webhook(WebhookBase):
    id: int
    created_at: datetime
    last_triggered_at: Optional[datetime] = None
    failure_count: int = 0

    class Config:
        from_attributes = True
