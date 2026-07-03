from app.schemas.intent_schema import IntentSchema

class ResearchDecisionService:
    def decide(self, intent_data: dict) -> dict:
        intent = intent_data.get("intent", "General Chat")
        confidence = intent_data.get("confidence", 1.0)
        complexity = intent_data.get("complexity", 1)
        topics = intent_data.get("topics_count", 1)
        needs_latest = intent_data.get("needs_latest_info", False)
        needs_sources = intent_data.get("needs_multiple_sources", False)
        
        # Calculate research score
        score = 0
        if intent in ["Research", "Comparison", "Decision Making", "Multi-Step Research"]:
            score += 40
        elif intent in ["Knowledge Question", "Coding Help"]:
            score += 20
            
        score += (complexity * 3)
        score += (topics * 5)
        
        if needs_latest:
            score += 10
        if needs_sources:
            score += 20
            
        # Fallback for low confidence
        if confidence < 0.6 and score > 50:
            score = 45 # downgrade to Knowledge Answer
            
        score = min(100, max(0, score))
        
        # Routing logic
        mode = "casual_chat"
        if score > 50:
            mode = "deep_research"
        elif score > 20:
            mode = "knowledge_answer"
            
        return {
            "research_score": score,
            "mode": mode,
            "intent": intent
        }
