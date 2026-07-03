from typing import Dict, Any
from app.schemas.insight import StructuredInsights

class InsightService:
    def process_insights(self, llm_output: StructuredInsights) -> Dict[str, Any]:
        """
        Processes and categorizes the LLM insights output.
        """
        if not llm_output:
            return {}
            
        trend_analysis = [i.model_dump() for i in llm_output.insights if "trend" in i.category.lower() or "pattern" in i.category.lower()]
        comparisons = [i.model_dump() for i in llm_output.insights if "compar" in i.category.lower()]
        
        return {
            "insights": [i.model_dump() for i in llm_output.insights],
            "trend_analysis": trend_analysis,
            "comparisons": comparisons,
            "opportunities": llm_output.opportunities,
            "risks": llm_output.risks,
            "limitations": llm_output.limitations,
            "future_research": llm_output.future_research,
            "strategic_takeaways": llm_output.strategic_takeaways
        }
