import time
import json
from typing import List, Dict, Any
from app.services.gemini_service import GeminiService
from app.services.validation.confidence_service import ConfidenceService, ConfidenceResult
from app.prompts.confidence_prompt import CONFIDENCE_SYSTEM_PROMPT
from app.utils.logger import log

class ConfidenceScoringAgent:
    """Agent responsible for assigning the final 0-100 confidence score."""
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.service = ConfidenceService()

    async def score(
        self, 
        unique_evidence: List[Dict[str, Any]], 
        credibility_scores: Dict[str, Any], 
        conflicts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        log.info(f"ConfidenceScoringAgent started. Input count: {len(unique_evidence)}")
        start_time = time.time()
        
        if not unique_evidence:
            return {}
            
        try:
            context = {
                "evidence": unique_evidence,
                "credibility": credibility_scores,
                "conflicts": conflicts
            }
            context_json = json.dumps(context, indent=2)
            prompt = f"Analyze the evidence and context to assign confidence scores:\n\n{context_json}"
            
            llm_output: ConfidenceResult = await self.gemini_service.structured_chat(
                prompt=prompt,
                schema=ConfidenceResult,
                system_prompt=CONFIDENCE_SYSTEM_PROMPT
            )
            
            scores = self.service.process_scores(llm_output)
            
            duration = time.time() - start_time
            log.info(f"ConfidenceScoringAgent completed in {duration:.4f}s. Output count: {len(scores)}")
            
            return scores
        except Exception as e:
            duration = time.time() - start_time
            log.error(f"ConfidenceScoringAgent failed after {duration:.4f}s: {e}")
            return {}
