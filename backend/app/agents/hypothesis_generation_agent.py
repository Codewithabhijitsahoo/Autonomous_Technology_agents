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
            res: HypothesisSchema = await self.gemini_service.structured_chat(
                prompt=f"Generate a hypothesis for this structured query: {structured_query}",
                schema=HypothesisSchema,
                system_prompt="You are a Hypothesis Generation Agent. Provide a preliminary internal answer and assumptions based on your internal knowledge."
            )
            log.info(f"HypothesisGenerationAgent finished in {time.time() - start_time:.2f}s")
            return res.model_dump()
        except Exception as e:
            log.error(f"HypothesisGenerationAgent error: {e}")
            raise e
