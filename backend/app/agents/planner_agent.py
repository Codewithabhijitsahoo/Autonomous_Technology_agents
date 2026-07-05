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
            # TASK 3: Improve Search Query Generation
            prompt = f"Create a research plan for the following query: {query}\n\nIMPORTANT: Do NOT generate one broad search task. Instead, generate multiple highly focused search tasks (e.g. 5-10 tasks). Every entity, person, or sub-topic should have its own optimized search query mapping directly to available search tools (Web Search, Wikipedia, Arxiv, News)."
            plan: ResearchPlanSchema = await self.gemini_service.structured_chat(
                prompt=prompt,
                schema=ResearchPlanSchema,
                system_prompt=PLANNER_SYSTEM_PROMPT,
                task_type="planning"
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
