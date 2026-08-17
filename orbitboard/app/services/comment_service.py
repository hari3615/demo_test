from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

def create_comment(db: Session, comment: CommentCreate, author_id: int):
    db_comment = Comment(**comment.model_dump(), author_id=author_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_for_task(db: Session, task_id: int):
    return db.query(Comment).filter(Comment.task_id == task_id).all()
