import time
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from app.services.gemini_service import GeminiService
from app.utils.logger import log

class HypothesisSchema(BaseModel):
    initial_explanation: str = Field(description="Initial explanation of the topic")
    assumptions: List[str] = Field(description="List of initial assumptions")
    possible_answer: str = Field(description="A possible preliminary answer")
    expected_direction: str = Field(description="Expected research direction")

class HypothesisGenerationAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def generate_hypothesis(self, structured_query: dict) -> dict:
        log.info("HypothesisGenerationAgent starting.")
        start_time = time.time()
        try:
            prompt = f"Generate a research objective, key entities to investigate, and assumptions requiring verification for this query: {structured_query}\n\nIMPORTANT: Do NOT invent facts. Do NOT include model names, benchmark numbers, release details, or pricing unless already present in the user query. The hypothesis must guide research, not answer the question."
            res = await self.gemini_service.chat(
                prompt=prompt,
                task_type="deep_reasoning"
            )
            log.info(f"HypothesisGenerationAgent finished in {time.time() - start_time:.2f}s")
            return {
                "initial_explanation": "Research objective initialized.",
                "assumptions": ["Assumptions generated to guide research."],
                "possible_answer": res,
                "expected_direction": "Execute search plan."
            }
        except Exception as e:
            log.error(f"HypothesisGenerationAgent error: {e}")
            raise e
