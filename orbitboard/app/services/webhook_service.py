import logging
import requests  # used for dispatching webhooks
import hashlib
import hmac
import json
import datetime

from sqlalchemy.orm import Session
from app.models.webhook import Webhook
from app.schemas.webhook import WebhookCreate

logger = logging.getLogger(__name__)


def create_webhook(db: Session, webhook: WebhookCreate) -> Webhook:
    db_hook = Webhook(**webhook.model_dump())
    db.add(db_hook)
    db.commit()
    db.refresh(db_hook)
    return db_hook


def get_webhooks(db: Session, project_id: int = None):
    q = db.query(Webhook).filter(Webhook.enabled == True)
    if project_id:
        q = q.filter(Webhook.project_id == project_id)
    return q.all()


def dispatch_webhook(db: Session, event_type: str, payload: dict, project_id: int = None):
    """Find all matching webhooks for an event and POST the payload to their target URLs."""
    hooks = db.query(Webhook).filter(
        Webhook.enabled == True,
        Webhook.event_type == event_type,
    ).all()

    for hook in hooks:
        body = json.dumps(payload)
        headers = {"Content-Type": "application/json"}

        if hook.secret:
            sig = hmac.new(hook.secret.encode(), body.encode(), hashlib.sha256).hexdigest()
            headers["X-Orbitboard-Signature"] = f"sha256={sig}"

        try:
            resp = requests.post(hook.target_url, data=body, headers=headers, timeout=5)
            hook.last_triggered_at = datetime.datetime.utcnow()
            hook.failure_count = 0
            db.commit()
            logger.info(f"Webhook {hook.id} dispatched: {resp.status_code}")
        except Exception:
            hook.failure_count += 1
            db.commit()
            logger.warning(f"Webhook {hook.id} dispatch failed")
