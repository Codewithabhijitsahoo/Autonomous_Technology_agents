import time
from typing import List
from pydantic import BaseModel, Field
from app.services.gemini_service import GeminiService
from app.utils.logger import log

class MergedQuerySchema(BaseModel):
    intent: str = Field(description="The primary intent of the user query (e.g. casual_chat, knowledge_answer, deep_research)")
    complexity: str = Field(description="Complexity level: Simple, Medium, Complex, Very Complex based on query length, number of requested topics, comparisons, time range, and deliverables.")
    keywords: List[str] = Field(description="Search keywords")
    entities: List[str] = Field(description="Key entities extracted from the query")
    domain: str = Field(description="The general domain or subject area")
    needs_research: bool = Field(description="True if the query requires external research")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0.")

from app.services.fast_intent_service import fast_intent_classifier

class QueryUnderstandingAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def understand_query(self, query: str) -> dict:
        log.info("QueryUnderstandingAgent starting.")
        start_time = time.time()
        
        # TASK 1 & 3: Ultra Fast Rule Engine & Complexity Detection
        fast_result = fast_intent_classifier.classify(query)
        if fast_result.get("fast_path_activated"):
            log.info(f"Fast Path Activated! Rule Matched: {fast_result.get('rule_matched')}. Gemini Skipped.")
            return fast_result

        # TASK 2 & 6: Merge Understanding + Intent Detection (Single Gemini Call)
        log.info("LLM Classification Required.")
        try:
            res: MergedQuerySchema = await self.gemini_service.structured_chat(
                prompt=f"Analyze and classify this user query: {query}",
                schema=MergedQuerySchema,
                system_prompt="You are a Query Understanding Agent. Extract structured information and intent from the user query. Output intent strictly as 'casual_chat', 'knowledge_answer', or 'deep_research'."
            )
            log.info(f"QueryUnderstandingAgent finished in {time.time() - start_time:.2f}s")
            
            dump = res.model_dump()
            dump["mode"] = dump["intent"] # Align mode with intent for intent_router_node
            return dump
        except Exception as e:
            log.error(f"QueryUnderstandingAgent error: {e}")
            raise e
