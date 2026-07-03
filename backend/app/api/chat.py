import time
import json
from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.graph.builder import graph
from app.utils.logger import log

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Accepts a user query, invokes the LangGraph, and returns the reviewed report, 
    quality scores, and quality report (Step 9).
    """
    log.info(f"API Route: Received chat query -> {request.query}")
    
    initial_state = {
        "query": request.query,
        "messages": [],
        "response": None,
        "steps": [],
        "metadata": {},
        "errors": [],
        "sources": [],
        "execution_time": 0.0
    }
    
    try:
        log.info("Graph execution started")
        start_time = time.time()
        
        final_state = await graph.ainvoke(initial_state)
        
        duration = time.time() - start_time
        log.info(f"Graph completion successful - Total Duration: {duration:.4f}s")
        
        if final_state.get("errors"):
            log.warning(f"Graph executed with errors: {final_state['errors']}")
            
        response_text = final_state.get("final_report", final_state.get("reviewed_report", "No response."))
        
        return ChatResponse(
            success=True,
            response=response_text,
            mode=final_state.get("mode", "deep_research"),
            intent=final_state.get("intent", "Unknown"),
            research_score=final_state.get("research_score", 0),
            citations=final_state.get("citations", [])
        )
        
    except Exception as e:
        log.error(f"Chat endpoint graph execution error encountered: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while executing the LangGraph workflow."
        )
