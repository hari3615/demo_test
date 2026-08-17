from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.plugin import Plugin, PluginCreate, PluginRun
from app.services import plugin_service

router = APIRouter()


@router.post("/", response_model=Plugin)
def register_plugin(plugin: PluginCreate, db: Session = Depends(get_db)):
    return plugin_service.register_plugin(db, plugin)


@router.get("/", response_model=List[Plugin])
def list_plugins(db: Session = Depends(get_db)):
    return plugin_service.get_plugins(db)


@router.post("/run/")
def run_plugin(payload: PluginRun, db: Session = Depends(get_db)):
    """
    Load and run a registered plugin.

    BUG: If the plugin's stored module_path is not an installed Python module,
    this endpoint will crash with HTTP 500 (unhandled ModuleNotFoundError).
    """
    result = plugin_service.run_plugin(db, plugin_name=payload.plugin_name, payload=payload.payload)
    return {"status": "ok", "result": result}
