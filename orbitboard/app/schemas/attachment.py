from pydantic import BaseModel

class AttachmentBase(BaseModel):
    filename: str
    file_path: str

class AttachmentCreate(AttachmentBase):
    task_id: int

class Attachment(AttachmentBase):
    id: int
    task_id: int

    class Config:
        from_attributes = True
