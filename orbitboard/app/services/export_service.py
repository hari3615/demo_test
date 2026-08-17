import json
from app.services import notification_service

def export_project(project_id: int):
    # Dummy export logic
    export_data = {
        "project_id": project_id,
        "name": f"Project {project_id}",
        "tasks": [],
        "notifications": notification_service.get_all_notifications()
    }
    return json.dumps(export_data)
