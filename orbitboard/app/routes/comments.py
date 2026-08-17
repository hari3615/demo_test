from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.comment import Comment, CommentCreate
from app.services import comment_service

router = APIRouter()

@router.post("/", response_model=Comment)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    # Hardcoding author_id
    return comment_service.create_comment(db=db, comment=comment, author_id=1)

@router.get("/task/{task_id}", response_model=List[Comment])
def read_comments(task_id: int, db: Session = Depends(get_db)):
    return comment_service.get_comments_for_task(db, task_id=task_id)
