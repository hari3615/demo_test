from fastapi import FastAPI

from app.config import settings
from app.routes import auth_router, project_router, task_router, comment_router, search_router, admin_router, rbac_router, audit_router, webhook_router, plugin_router

app = FastAPI(title=settings.app_name)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(project_router, prefix="/projects", tags=["projects"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(comment_router, prefix="/comments", tags=["comments"])
app.include_router(search_router, prefix="/search", tags=["search"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(rbac_router, prefix="/rbac", tags=["rbac"])
app.include_router(audit_router, prefix="/audit", tags=["audit"])
app.include_router(webhook_router, prefix="/webhooks", tags=["webhooks"])
app.include_router(plugin_router, prefix="/plugins", tags=["plugins"])

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.app_name} API"}
