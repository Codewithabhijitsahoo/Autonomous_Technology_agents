from typing import Any, Dict, Optional
from pydantic import BaseModel

class ErrorDetail(BaseModel):
    type: str
    message: str
    agent: Optional[str] = None
    node: Optional[str] = None
    retryable: bool = False

class ApiResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[ErrorDetail] = None

def success_response(data: Any) -> Dict[str, Any]:
    return {"success": True, "data": data}

def error_response(type: str, message: str, agent: str = None, node: str = None, retryable: bool = False) -> Dict[str, Any]:
    return {
        "success": False,
        "error": {
            "type": type,
            "message": message,
            "agent": agent,
            "node": node,
            "retryable": retryable
        }
    }
