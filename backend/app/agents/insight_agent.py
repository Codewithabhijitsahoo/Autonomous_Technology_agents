import time
import json
from typing import Dict, Any
from app.services.gemini_service import GeminiService
from app.services.insight_service import InsightService
from app.prompts.insight_prompt import INSIGHT_GENERATION_PROMPT
from app.schemas.insight import StructuredInsights
from app.utils.logger import log

class InsightGenerationAgent:
    """Agent responsible for reasoning over synthesized knowledge and extracting insights."""
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.service = InsightService()

    async def generate_insights(self, knowledge: Dict[str, Any], retries: int = 0) -> Dict[str, Any]:
        log.info("InsightGenerationAgent started analysis.")
        start_time = time.time()
        
        if not knowledge or not knowledge.get("entities"):
            log.warning("No knowledge provided for insight generation.")
            return {}

        # Limit JSON length just in case it's absurdly large, though Gemini context is 1M+ tokens
        knowledge_json = json.dumps(knowledge, indent=2)
        prompt = f"Analyze the following synthesized knowledge to generate deep insights:\n\n{knowledge_json}"
        
        for attempt in range(retries + 1):
            try:
                log.info(f"Generating insights (Attempt {attempt+1}/{retries+1})")
                llm_output: StructuredInsights = await self.gemini_service.structured_chat(
                    prompt=prompt,
                    schema=StructuredInsights,
                    system_prompt=INSIGHT_GENERATION_PROMPT
                )
                
                result = self.service.process_insights(llm_output)
                
                duration = time.time() - start_time
                log.info(f"InsightGenerationAgent completed in {duration:.4f}s. Generated {len(result.get('insights', []))} insights.")
                return result
                
            except Exception as e:
                log.warning(f"Insight generation attempt {attempt+1} failed: {e}")
                if attempt == retries:
                    log.error(f"InsightGenerationAgent failed completely: {e}")
                    return {}
