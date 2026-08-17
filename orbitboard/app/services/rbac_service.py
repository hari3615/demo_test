from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.role import Role, Permission, UserRole
from app.schemas.role import RoleCreate, PermissionCreate


def create_permission(db: Session, permission: PermissionCreate) -> Permission:
    db_perm = Permission(**permission.model_dump())
    db.add(db_perm)
    db.commit()
    db.refresh(db_perm)
    return db_perm


def get_permissions(db: Session) -> List[Permission]:
    return db.query(Permission).all()


def create_role(db: Session, role: RoleCreate) -> Role:
    db_role = Role(name=role.name, description=role.description)
    if role.permission_ids:
        perms = db.query(Permission).filter(Permission.id.in_(role.permission_ids)).all()
        db_role.permissions = perms
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_roles(db: Session) -> List[Role]:
    return db.query(Role).all()


def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    return db.query(Role).filter(Role.name == name).first()


def assign_role_to_user(db: Session, user_id: int, role_id: int) -> UserRole:
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role


def get_user_roles(db: Session, user_id: int) -> List[Role]:
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()
    return [ur.role for ur in user_roles]


def check_permission(db: Session, user_id: int, resource: str, action: str) -> bool:
    """Check if a user has a specific permission via their roles."""
    user_roles = get_user_roles(db, user_id)
    for role in user_roles:
        for perm in role.permissions:
            if perm.resource == resource and perm.action == action:
                return True
    return False
