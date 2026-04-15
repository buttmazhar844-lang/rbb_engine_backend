from typing import Any, Dict

def success(message: str, data: Any = None) -> Dict[str, Any]:
    """Standard success response format"""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response

def error(message: str, details: Any = None) -> Dict[str, Any]:
    """Standard error response format"""
    response = {
        "success": False,
        "message": message
    }
    if details is not None:
        response["details"] = details
    return response