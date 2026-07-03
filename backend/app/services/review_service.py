from typing import Dict, Any
from app.schemas.review import ReviewResult

class ReviewService:
    def process_review(self, llm_output: ReviewResult) -> Dict[str, Any]:
        """
        Processes the LLM output into graph state variables.
        """
        if not llm_output:
            return {}
            
        quality_report = {
            "strengths": llm_output.strengths,
            "weaknesses": llm_output.weaknesses,
            "missing_topics": llm_output.missing_topics,
            "unsupported_claims": llm_output.unsupported_claims,
            "contradictions": llm_output.contradictions,
            "formatting_problems": llm_output.formatting_problems
        }
        
        return {
            "reviewed_report": llm_output.reviewed_report,
            "quality_scores": llm_output.quality_scores.model_dump(),
            "quality_report": quality_report,
            "improvements": llm_output.improvements_made,
            "issues_found": [issue.model_dump() for issue in llm_output.issues_found],
            "review_summary": f"Report scored {llm_output.quality_scores.overall_score}/100. Found {len(llm_output.issues_found)} issues and applied {len(llm_output.improvements_made)} auto-corrections."
        }
