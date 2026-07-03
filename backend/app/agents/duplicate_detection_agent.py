import time
import json
from typing import List, Dict, Any, Tuple
from app.services.gemini_service import GeminiService
from app.services.validation.duplicate_service import DuplicateService, DuplicateResult
from app.prompts.duplicate_prompt import DUPLICATE_SYSTEM_PROMPT
from app.utils.logger import log

class DuplicateDetectionAgent:
    """Agent responsible for detecting exact and semantic duplicates."""
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.service = DuplicateService()

    async def detect(self, raw_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        log.info(f"DuplicateDetectionAgent started. Input count: {len(raw_evidence)}")
        start_time = time.time()
        
        if not raw_evidence:
            return {"unique_evidence": [], "duplicate_groups": [], "removed_duplicates": []}
            
        try:
            evidence_json = json.dumps(raw_evidence, indent=2)
            prompt = f"Analyze these evidence items for duplicates:\n\n{evidence_json}"
            
            llm_output: DuplicateResult = await self.gemini_service.structured_chat(
                prompt=prompt,
                schema=DuplicateResult,
                system_prompt=DUPLICATE_SYSTEM_PROMPT
            )
            
            result = self.service.process_duplicates(raw_evidence, llm_output)
            
            duration = time.time() - start_time
            log.info(f"DuplicateDetectionAgent completed in {duration:.4f}s. Unique count: {len(result['unique_evidence'])}")
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            log.error(f"DuplicateDetectionAgent failed after {duration:.4f}s: {e}")
            return {"unique_evidence": raw_evidence, "duplicate_groups": [], "removed_duplicates": []}
