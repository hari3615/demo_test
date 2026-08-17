from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.webhook import Webhook, WebhookCreate
from app.services import webhook_service

router = APIRouter()


@router.post("/", response_model=Webhook)
def create_webhook(webhook: WebhookCreate, db: Session = Depends(get_db)):
    return webhook_service.create_webhook(db, webhook)


@router.get("/", response_model=List[Webhook])
def list_webhooks(project_id: int = None, db: Session = Depends(get_db)):
    return webhook_service.get_webhooks(db, project_id=project_id)


@router.post("/dispatch/")
def dispatch(event_type: str, payload: dict, db: Session = Depends(get_db)):
    webhook_service.dispatch_webhook(db, event_type=event_type, payload=payload)
    return {"status": "dispatched"}
