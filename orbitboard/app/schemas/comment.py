from pydantic import BaseModel

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    task_id: int

class Comment(CommentBase):
    id: int
    task_id: int
    author_id: int

    class Config:
        from_attributes = True
