import time
import json
from typing import List, Dict, Any
from app.services.gemini_service import GeminiService
from app.services.validation.conflict_service import ConflictService, ConflictResult
from app.prompts.conflict_prompt import CONFLICT_SYSTEM_PROMPT
from app.utils.logger import log

class ConflictDetectionAgent:
    """Agent responsible for grouping conflicting claims."""
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.service = ConflictService()

    async def detect(self, unique_evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        log.info(f"ConflictDetectionAgent started. Input count: {len(unique_evidence)}")
        start_time = time.time()
        
        if len(unique_evidence) < 2:
            return []
            
        try:
            evidence_json = json.dumps(unique_evidence, indent=2)
            prompt = f"Analyze these evidence items for conflicting claims:\n\n{evidence_json}"
            
            llm_output: ConflictResult = await self.gemini_service.structured_chat(
                prompt=prompt,
                schema=ConflictResult,
                system_prompt=CONFLICT_SYSTEM_PROMPT
            )
            
            conflicts = self.service.process_conflicts(llm_output)
            
            duration = time.time() - start_time
            log.info(f"ConflictDetectionAgent completed in {duration:.4f}s. Conflicts found: {len(conflicts)}")
            
            return conflicts
        except Exception as e:
            duration = time.time() - start_time
            log.error(f"ConflictDetectionAgent failed after {duration:.4f}s: {e}")
            return []
