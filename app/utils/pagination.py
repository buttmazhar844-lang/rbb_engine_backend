from typing import Any, Dict, List
from sqlalchemy.orm import Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    limit: int = 50
    offset: int = 0

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    limit: int
    offset: int
    has_next: bool

def paginate_query(query: Query, params: PaginationParams) -> PaginatedResponse:
    """Apply pagination to SQLAlchemy query"""
    total = query.count()
    items = query.offset(params.offset).limit(params.limit).all()
    
    return PaginatedResponse(
        items=items,
        total=total,
        limit=params.limit,
        offset=params.offset,
        has_next=(params.offset + params.limit) < total
    )