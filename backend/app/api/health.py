from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def get_health():
    """Returns application health and status."""
    return {
        "success": True,
        "data": {
            "api_status": "healthy",
            "gemini_status": "connected",
            "graph_status": "compiled",
            "registered_agents": ["Planner", "Validator", "Collector", "Knowledge", "Insight", "Review"],
            "registered_tools": ["Web Search", "Wikipedia", "Arxiv", "News"],
            "application_version": settings.app_version
        }
    }
