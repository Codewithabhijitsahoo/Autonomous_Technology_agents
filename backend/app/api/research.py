from fastapi import APIRouter

router = APIRouter(prefix="/research", tags=["research"])

@router.post("")
async def start_research():
    """
    Placeholder endpoint for triggering the Deep Research workflow.
    """
    return {"message": "Research endpoint not implemented yet."}
