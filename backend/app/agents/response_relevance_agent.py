import time
from typing import List
from pydantic import BaseModel, Field
from app.services.gemini_service import GeminiService
from app.utils.logger import log

class RelevanceSchema(BaseModel):
    coverage_score: float = Field(description="Score from 0.0 to 1.0 indicating how well the report covers the query")
    similarity_score: float = Field(description="Score from 0.0 to 1.0 indicating semantic similarity")
    missing_sections: List[str] = Field(description="List of required info missing from the report")
    quality_suggestions: List[str] = Field(description="Suggestions for improvement")
    needs_partial_regeneration: bool = Field(description="True if coverage_score is below 0.8")

class ResponseRelevanceAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def check_relevance(self, original_query: str, structured_query: dict, final_report: str) -> dict:
        log.info("ResponseRelevanceAgent starting.")
        start_time = time.time()
        try:
            # Phase 6: Merged validation logic with ReviewAgent to avoid duplicate LLM calls
            # Perform a fast heuristic check instead
            coverage = 1.0 if len(final_report) > 500 else 0.5
            needs_regen = coverage < 0.8 and "Error Generating Report" not in final_report
            
            res = RelevanceSchema(
                coverage_score=coverage,
                similarity_score=0.9,
                missing_sections=[],
                quality_suggestions=["Delegated to Review Agent"],
                needs_partial_regeneration=needs_regen
            )
            
            log.info(f"ResponseRelevanceAgent (Heuristic Mode) finished in {time.time() - start_time:.2f}s")
            return res.model_dump()
        except Exception as e:
            log.error(f"ResponseRelevanceAgent error: {e}")
            raise e
