from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.schemas.audit_log import AuditLog
from app.services import audit_service

router = APIRouter()


@router.get("/", response_model=List[AuditLog])
def get_audit_logs(
    resource_type: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    limit: int = Query(100),
    db: Session = Depends(get_db),
):
    return audit_service.get_audit_logs(db, resource_type=resource_type, user_id=user_id, limit=limit)
