import time
from app.services.gemini_service import GeminiService
from app.prompts.planner_prompt import PLANNER_SYSTEM_PROMPT
from app.schemas.planner import ResearchPlanSchema
from app.utils.logger import log

class PlannerAgent:
    """
    Agent responsible for analyzing the user's query and generating a structured research plan.
    It uses GeminiService for all AI interactions to maintain clean architecture.
    """
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def generate_plan(self, query: str) -> ResearchPlanSchema:
        """
        Generates a structured research plan based on the user's query.
        """
        log.info(f"PlannerAgent starting plan generation for query: '{query}'")
        start_time = time.time()
        
        try:
            # We call the structured chat from GeminiService to enforce JSON output matching the schema
            plan: ResearchPlanSchema = await self.gemini_service.structured_chat(
                prompt=f"Create a detailed research plan for the following query: {query}",
                schema=ResearchPlanSchema,
                system_prompt=PLANNER_SYSTEM_PROMPT
            )
            
            duration = time.time() - start_time
            log.info(f"PlannerAgent finished successfully in {duration:.4f}s")
            
            # Log the extracted details as requested
            log.info(f"Extracted tasks count: {len(plan.tasks)}")
            log.info(f"Recommended tools: {plan.recommended_tools}")
            
            return plan
            
        except Exception as e:
            duration = time.time() - start_time
            log.error(f"PlannerAgent encountered an error after {duration:.4f}s: {e}")
            raise e
