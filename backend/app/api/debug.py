from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/system")
async def get_system_debug():
    """Returns system internals for debugging."""
    return {
        "success": True,
        "data": {
            "loaded_agents": ["planner_agent", "evidence_collector_agent", "duplicate_detection_agent", "insight_agent", "review_agent"],
            "loaded_graph": "Validation Pipeline -> Knowledge -> Insight -> Report -> Review",
            "loaded_tools": ["search_tool", "wikipedia_tool", "arxiv_tool"],
            "loaded_prompts": ["duplicate_prompt", "credibility_prompt", "insight_prompt", "review_prompt", "knowledge_prompt"],
            "current_configuration": {
                "environment": settings.environment,
                "model": settings.gemini_model,
                "max_tokens": settings.gemini_max_tokens
            }
        }
    }
