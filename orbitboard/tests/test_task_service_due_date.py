import pytest
from datetime import datetime, timezone
from app.services import task_service
from app.models.task import Task

class MockTask:
    def __init__(self, id, started_at, due_date=None, estimate_days=0.0):
        self.id = id
        self.started_at = started_at
        self.due_date = due_date
        self.estimate_days = estimate_days

def test_recompute_due_date_normal():
    started = datetime(2023, 10, 1, 10, 0, tzinfo=timezone.utc)
    task = MockTask(id=1, started_at=started)
    
    new_date = task_service.recompute_due_date(task, 2.0)
    assert new_date is not None
    assert task.estimate_days == 2.0

def test_recompute_due_date_large_estimate():
    started = datetime(2023, 10, 1, 10, 0, tzinfo=timezone.utc)
    task = MockTask(id=2, started_at=started)
    
    new_date = task_service.recompute_due_date(task, 10.5)
    assert new_date is not None
    assert task.estimate_days == 10.5

def test_recompute_due_date_on_unstarted_task():
    # This test MUST fail because task.started_at is None
    task = MockTask(id=3, started_at=None)
    # The buggy implementation will attempt to access task.started_at.tzinfo
    # raising an AttributeError
    task_service.recompute_due_date(task, 3.0)
