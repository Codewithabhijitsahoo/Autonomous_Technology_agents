import time
from typing import Dict, Any
from app.utils.logger import log

class IntentRouterAgent:
    def __init__(self):
        # The IntentRouterAgent now performs pure routing without LLM calls.
        pass

    def route_intent(self, structured_query: Dict[str, Any]) -> dict:
        log.info("IntentRouterAgent routing based on structured query.")
        start_time = time.time()
        
        try:
            intent = structured_query.get("intent", "deep_research").lower()
            confidence = structured_query.get("confidence", 1.0)
            requires_research = structured_query.get("needs_research", True)
            
            # Logic: If confidence is very low, force deep research to ensure accuracy
            if confidence < 0.4:
                intent = "deep_research"
                
            # Direct mapping from Intent to Node mode
            if intent == "casual_chat" and not requires_research:
                mode = "casual_chat"
                research_score = 0
            elif intent == "knowledge_answer" and not requires_research:
                mode = "knowledge_answer"
                research_score = 50
            else:
                mode = "deep_research"
                research_score = 100
                
            log.info(f"IntentRouterAgent finished in {time.time() - start_time:.4f}s. Routed to: {mode}")
            
            return {
                "intent": intent,
                "research_score": research_score,
                "mode": mode
            }
        except Exception as e:
            log.error(f"IntentRouterAgent error: {e}")
            raise e
