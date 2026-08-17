from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate

def create_project(db: Session, project: ProjectCreate, owner_id: int):
    db_project = Project(**project.model_dump(), owner_id=owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()
