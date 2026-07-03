import time
from typing import List
from pydantic import BaseModel, Field
from app.services.gemini_service import GeminiService
from app.utils.logger import log

class StructuredQuerySchema(BaseModel):
    intent: str = Field(description="The primary intent of the user query")
    entities: List[str] = Field(description="Key entities extracted from the query")
    keywords: List[str] = Field(description="Search keywords")
    domain: str = Field(description="The general domain or subject area")
    complexity: str = Field(description="Complexity level: easy, medium, hard")
    format: str = Field(description="The requested output format")

class QueryUnderstandingAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def understand_query(self, query: str) -> dict:
        log.info("QueryUnderstandingAgent starting.")
        start_time = time.time()
        try:
            res: StructuredQuerySchema = await self.gemini_service.structured_chat(
                prompt=f"Analyze this user query: {query}",
                schema=StructuredQuerySchema,
                system_prompt="You are a Query Understanding Agent. Extract structured information from the user query."
            )
            log.info(f"QueryUnderstandingAgent finished in {time.time() - start_time:.2f}s")
            return res.model_dump()
        except Exception as e:
            log.error(f"QueryUnderstandingAgent error: {e}")
            raise e
