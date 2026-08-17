from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import search_service

router = APIRouter()

@router.get("/")
def search(q: str = Query(...), db: Session = Depends(get_db)):
    return search_service.search_content(db, q)
