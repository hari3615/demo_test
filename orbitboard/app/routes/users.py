from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.routes.auth import get_current_user
from app.services import auth_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Retrieves profile stats of currently authenticated active caller."""
    return current_user

@router.patch("/me", response_model=UserOut)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Updates fields on current user profile."""
    if user_update.email is not None and user_update.email != current_user.email:
        # Check uniqueness
        duplicate = db.query(User).filter(User.email == user_update.email).first()
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email in use."
            )
        current_user.email = user_update.email
    
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
        
    if user_update.password is not None:
        current_user.hashed_password = auth_service.get_password_hash(user_update.password)
        
    if user_update.is_active is not None and current_user.is_superuser:
        current_user.is_active = user_update.is_active

    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/", response_model=List[UserOut])
def list_system_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lists all users (requires active user session)."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users
