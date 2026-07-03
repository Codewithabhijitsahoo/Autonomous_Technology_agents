import time
import json
from typing import List, Dict, Any
from app.services.gemini_service import GeminiService
from app.services.validation.credibility_service import CredibilityService, CredibilityResult
from app.prompts.credibility_prompt import CREDIBILITY_SYSTEM_PROMPT
from app.utils.logger import log

class SourceCredibilityAgent:
    """Agent responsible for assigning a 0-100 credibility score."""
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.service = CredibilityService()

    async def analyze(self, unique_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        log.info(f"SourceCredibilityAgent started. Input count: {len(unique_evidence)}")
        start_time = time.time()
        
        if not unique_evidence:
            return {}
            
        try:
            evidence_json = json.dumps(unique_evidence, indent=2)
            prompt = f"Analyze source credibility for these evidence items:\n\n{evidence_json}"
            
            llm_output: CredibilityResult = await self.gemini_service.structured_chat(
                prompt=prompt,
                schema=CredibilityResult,
                system_prompt=CREDIBILITY_SYSTEM_PROMPT
            )
            
            scores = self.service.process_scores(llm_output)
            
            duration = time.time() - start_time
            log.info(f"SourceCredibilityAgent completed in {duration:.4f}s. Output count: {len(scores)}")
            
            return scores
        except Exception as e:
            duration = time.time() - start_time
            log.error(f"SourceCredibilityAgent failed after {duration:.4f}s: {e}")
            return {}
