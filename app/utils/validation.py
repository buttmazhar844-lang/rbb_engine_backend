from fastapi import HTTPException
from typing import Any, Dict, List
from app.utils.logger import logger

def validate_positive_integer(value: int, field_name: str) -> None:
    """Validate that a value is a positive integer"""
    if not isinstance(value, int) or value <= 0:
        raise HTTPException(status_code=400, detail=f"{field_name} must be a positive integer")

def validate_grade_level(grade_level: int) -> None:
    """Validate grade level is within acceptable range"""
    if not isinstance(grade_level, int) or grade_level < 1 or grade_level > 12:
        raise HTTPException(status_code=400, detail="Grade level must be between 1 and 12")

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Validate that all required fields are present and not None"""
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    
    if missing_fields:
        raise HTTPException(
            status_code=400, 
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )

def handle_not_found(entity_name: str, entity_id: int) -> HTTPException:
    """Standardized not found error"""
    return HTTPException(
        status_code=404, 
        detail=f"{entity_name} with id {entity_id} not found"
    )

def handle_database_error(operation: str, entity_name: str) -> HTTPException:
    """Standardized database error handling"""
    logger.error(f"Database error during {operation} for {entity_name}")
    return HTTPException(
        status_code=500, 
        detail=f"Failed to {operation} {entity_name}"
    )

def validate_status_transition(current_status: str, new_status: str, valid_transitions: dict) -> None:
    """Validate status transitions are allowed"""
    if new_status not in valid_transitions.get(current_status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {current_status} to {new_status}"
        )

def validate_entity_exists(entity, entity_name: str, entity_id: int) -> None:
    """Validate that an entity exists, raise 404 if not"""
    if not entity:
        raise HTTPException(
            status_code=404,
            detail=f"{entity_name} with id {entity_id} not found"
        )