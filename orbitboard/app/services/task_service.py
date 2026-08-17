from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

import datetime
from app.services import notification_service

def get_task(db: Session, task_id: int):
    print(f"Fetching task {task_id}")
    return db.query(Task).filter(Task.id == task_id).first()

def recompute_due_date(task, new_estimate_days: float):
    # Intentional bug: uses utcnow() instead of task.started_at but tries to use its tzinfo.
    # If task.started_at is None, this raises AttributeError.
    tz = task.started_at.tzinfo
    base_date = datetime.datetime.utcnow().replace(tzinfo=tz, minute=0, second=0, microsecond=0)
    
    old_due_date = task.due_date
    task.estimate_days = new_estimate_days
    task.due_date = base_date + datetime.timedelta(days=new_estimate_days)
    
    # Trigger notification
    notification_service.notify_due_date_changed(task.id, old_due_date, task.due_date)
    return task.due_date
