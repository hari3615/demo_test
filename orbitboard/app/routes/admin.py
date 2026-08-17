from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import export_service, import_service

router = APIRouter()

class ImportPayload(BaseModel):
    blob: str

@router.get("/export/{project_id}")
def export_project(project_id: int):
    return {"data": export_service.export_project(project_id)}

@router.post("/import")
def import_project(payload: ImportPayload):
    try:
        data = import_service.import_project_from_blob(payload.blob)
        return {"status": "success", "data": str(data)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
