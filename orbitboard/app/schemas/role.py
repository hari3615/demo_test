from pydantic import BaseModel
from typing import Optional, List


class PermissionBase(BaseModel):
    name: str
    resource: str
    action: str


class PermissionCreate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int

    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []


class Role(RoleBase):
    id: int
    permissions: List[Permission] = []

    class Config:
        from_attributes = True


class UserRoleAssign(BaseModel):
    user_id: int
    role_id: int
