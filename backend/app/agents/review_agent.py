import time
import json
from typing import Dict, Any
from app.services.gemini_service import GeminiService
from app.services.review_service import ReviewService
from app.prompts.review_prompt import REVIEW_SYSTEM_PROMPT
from app.schemas.review import ReviewResult
from app.utils.logger import log

class ReviewAgent:
    """Agent responsible for QA, scoring, and auto-correcting the final report."""
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.service = ReviewService()

    async def review(self, report: str, knowledge: Dict[str, Any], insights: list, retries: int = 0) -> Dict[str, Any]:
        log.info("ReviewAgent started quality assurance.")
        start_time = time.time()
        
        if not report:
            log.warning("No report provided for review.")
            return {}

        payload = {
            "report_to_review": report,
            "reference_knowledge": knowledge.get("executive_summary", "No summary available"),
            "reference_insights": [i.get("title") for i in insights]
        }
        
        payload_json = json.dumps(payload, indent=2)
        prompt = f"Perform a comprehensive Quality Assurance review on the following report based on the reference material:\n\n{payload_json}"
        
        for attempt in range(retries + 1):
            try:
                log.info(f"Generating review (Attempt {attempt+1}/{retries+1})")
                llm_output: ReviewResult = await self.gemini_service.structured_chat(
                    prompt=prompt,
                    schema=ReviewResult,
                    system_prompt=REVIEW_SYSTEM_PROMPT
                )
                
                result = self.service.process_review(llm_output)
                
                duration = time.time() - start_time
                log.info(f"ReviewAgent completed in {duration:.4f}s. Score: {result['quality_scores']['overall_score']}")
                return result
                
            except Exception as e:
                log.warning(f"Review attempt {attempt+1} failed: {e}")
                if attempt == retries:
                    log.error(f"ReviewAgent failed completely: {e}")
                    # Safe fallback bypassing review failure
                    return {
                        "reviewed_report": report,
                        "quality_scores": {"overall_score": 0},
                        "quality_report": {"error": str(e)},
                        "improvements": [],
                        "issues_found": [{"issue_type": "System Error", "description": str(e), "severity": "major", "suggested_fix": "Retry"}],
                        "review_summary": "Review failed due to system exception."
                    }
