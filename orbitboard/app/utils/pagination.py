"""
app/utils/pagination.py

Generic pagination helper for list endpoints.
"""
from typing import TypeVar, List, Generic
from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel):
    items: List
    total: int
    page: int
    size: int
    pages: int


def paginate(items: List, page: int = 1, size: int = 20) -> Page:
    """Return a paginated slice of `items`."""
    if page < 1:
        page = 1
    if size < 1:
        size = 20

    total = len(items)
    pages = (total + size - 1) // size if total > 0 else 1
    start = (page - 1) * size
    end = start + size
    return Page(items=items[start:end], total=total, page=page, size=size, pages=pages)
