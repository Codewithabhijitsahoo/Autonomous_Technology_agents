import time
from app.services.gemini_service import GeminiService
from app.schemas.intent_schema import IntentSchema
from app.prompts.intent_router_prompt import INTENT_ROUTER_SYSTEM_PROMPT
from app.utils.logger import log

class IntentRouterAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def route_intent(self, query: str) -> dict:
        log.info("IntentRouterAgent analyzing query.")
        start_time = time.time()
        try:
            res: IntentSchema = await self.gemini_service.structured_chat(
                prompt=f"Classify this query: {query}",
                schema=IntentSchema,
                system_prompt=INTENT_ROUTER_SYSTEM_PROMPT
            )
            log.info(f"IntentRouterAgent finished in {time.time() - start_time:.2f}s")
            return res.model_dump()
        except Exception as e:
            log.error(f"IntentRouterAgent error: {e}")
            raise e
