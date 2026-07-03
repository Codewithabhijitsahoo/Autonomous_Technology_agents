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
            prompt = f"Original Query: {original_query}\nStructured Query: {structured_query}\nFinal Report: {final_report}"
            res: RelevanceSchema = await self.gemini_service.structured_chat(
                prompt=prompt,
                schema=RelevanceSchema,
                system_prompt="You are a Response Relevance Checker. Compare the final report against the user query. Determine if the report fully answers the request. If coverage is poor (< 0.8), set needs_partial_regeneration to true."
            )
            log.info(f"ResponseRelevanceAgent finished in {time.time() - start_time:.2f}s")
            return res.model_dump()
        except Exception as e:
            log.error(f"ResponseRelevanceAgent error: {e}")
            raise e
