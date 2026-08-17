from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.role import Role, RoleCreate, Permission, PermissionCreate, UserRoleAssign
from app.services import rbac_service

router = APIRouter()


@router.post("/permissions/", response_model=Permission)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return rbac_service.create_permission(db, permission)


@router.get("/permissions/", response_model=List[Permission])
def list_permissions(db: Session = Depends(get_db)):
    return rbac_service.get_permissions(db)


@router.post("/roles/", response_model=Role)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    existing = rbac_service.get_role_by_name(db, role.name)
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    return rbac_service.create_role(db, role)


@router.get("/roles/", response_model=List[Role])
def list_roles(db: Session = Depends(get_db)):
    return rbac_service.get_roles(db)


@router.post("/assign/")
def assign_role(payload: UserRoleAssign, db: Session = Depends(get_db)):
    rbac_service.assign_role_to_user(db, payload.user_id, payload.role_id)
    return {"status": "ok", "message": f"Role {payload.role_id} assigned to user {payload.user_id}"}


@router.get("/check/")
def check_permission(user_id: int, resource: str, action: str, db: Session = Depends(get_db)):
    has_perm = rbac_service.check_permission(db, user_id, resource, action)
    return {"user_id": user_id, "resource": resource, "action": action, "allowed": has_perm}
