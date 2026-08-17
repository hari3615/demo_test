import datetime
import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate

logger = logging.getLogger(__name__)


def log_event(
    db: Session,
    action: str,
    resource_type: str,
    resource_id: Optional[int] = None,
    user_id: Optional[int] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None,
) -> AuditLog:
    """Record a security/business-logic audit event."""
    entry = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    logger.info(f"[AUDIT] {action} on {resource_type}#{resource_id} by user {user_id}")
    return entry


def get_audit_logs(
    db: Session,
    resource_type: Optional[str] = None,
    user_id: Optional[int] = None,
    limit: int = 100,
) -> List[AuditLog]:
    query = db.query(AuditLog)
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    return query.order_by(AuditLog.created_at.desc()).limit(limit).all()
