# In-memory pub/sub of events to "notify" watchers
import logging

logger = logging.getLogger(__name__)
_event_log = []

def notify_due_date_changed(task_id: int, old_date, new_date):
    # Log the event for the export service to pick up
    payload = {
        "event": "DUE_DATE_CHANGED",
        "task_id": task_id,
        "old": old_date.isoformat() if old_date else None,
        "new": new_date.isoformat() if new_date else None
    }
    _event_log.append(payload)
    logger.info(f"Notification: Task {task_id} due date changed to {new_date}")

def get_all_notifications():
    # Return all notifications collected in memory
    return _event_log
