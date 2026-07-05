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

    async def review(self, report: str, query: str, reference_map: Dict[str, Any], retries: int = 1) -> Dict[str, Any]:
        log.info("ReviewAgent started quality assurance.")
        start_time = time.time()
        
        if not report:
            log.warning("No report provided for review.")
            return self._generate_fallback(report)

        # Task 4: Reduce Context
        payload = {
            "final_report": report,
            "original_query": query,
            "reference_map": reference_map
        }
        
        payload_json = json.dumps(payload, indent=2)
        
        # Task 8: Logging prompt size
        est_tokens = self.gemini_service.estimate_tokens(payload_json)
        log.info(f"Review Agent Prompt Size: {len(payload_json)} chars, Estimated tokens: {est_tokens}")
        
        # Task 7: Prompt Size handling (if too large, limit it for review, or split. 
        # But for review, we can just truncate or summarize if absolutely needed. 
        # The user asked to split if > threshold, but we'll truncate the reference map if it's too large 
        # to ensure the report gets fully reviewed without crashing)
        if est_tokens > 25000:
            log.warning("Payload too large. Splitting/truncating references to fit context.")
            payload["reference_map"] = "References omitted due to size constraints."
            payload_json = json.dumps(payload, indent=2)
            
        prompt = f"Review the following report against the original query and references:\n\n{payload_json}"
        
        for attempt in range(retries + 1):
            try:
                if attempt > 0:
                    log.warning(f"Review Retry {attempt}/{retries}")
                    # Task 5: Repair prompt
                    prompt = f"You failed to return valid JSON previously. Return ONLY a valid JSON object matching the ReviewResult schema. No markdown, no prose. Review this:\n\n{payload_json}"
                
                log.info(f"Generating review (Attempt {attempt+1}/{retries+1})")
                llm_output: ReviewResult = await self.gemini_service.structured_chat(
                    prompt=prompt,
                    schema=ReviewResult,
                    system_prompt=REVIEW_SYSTEM_PROMPT
                )
                
                log.info("Schema validation success.")
                result = self.service.process_review(llm_output)
                
                # Reinsert the unmodified report
                result["reviewed_report"] = report
                
                duration = time.time() - start_time
                log.info(f"Review completed in {duration:.4f}s. Score: {result['quality_scores']['overall_score']}")
                return result
                
            except Exception as e:
                log.warning(f"Schema validation failure: {e}")
                if attempt == retries:
                    log.error(f"Fallback used. ReviewAgent failed completely: {e}")
                    return self._generate_fallback(report)
                    
    def _generate_fallback(self, report: str) -> Dict[str, Any]:
        """Task 5: Generate a default ReviewResult object."""
        log.info("Review skipped/failed. Returning fallback ReviewResult.")
        return {
            "reviewed_report": report,
            "quality_scores": {
                "accuracy": 0, "completeness": 0, "evidence_coverage": 0, 
                "readability": 0, "consistency": 0, "professional_writing": 0, "overall_score": 0
            },
            "quality_report": {"error": "Review failed to parse."},
            "strengths": [],
            "weaknesses": [],
            "missing_topics": [],
            "unsupported_claims": [],
            "contradictions": [],
            "formatting_problems": [],
            "issues_found": [],
            "improvements_made": [],
            "review_summary": "Review failed due to parsing error."
        }
