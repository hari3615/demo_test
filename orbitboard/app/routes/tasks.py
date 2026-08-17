from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.task import Task, TaskCreate
from app.services import task_service

router = APIRouter()

@router.post("/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db=db, task=task)

@router.get("/", response_model=List[Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = task_service.get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_service.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

from app.schemas.task import TaskUpdateEstimate

@router.patch("/{task_id}/estimate", response_model=Task)
def update_task_estimate(task_id: int, update_data: TaskUpdateEstimate, db: Session = Depends(get_db)):
    db_task = task_service.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_service.recompute_due_date(db_task, update_data.estimate_days)
    db.commit()
    db.refresh(db_task)
    return db_task
