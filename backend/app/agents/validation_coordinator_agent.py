import time
from typing import List, Dict, Any
from app.services.validation.validation_service import ValidationCoordinatorService
from app.utils.logger import log

class ValidationCoordinatorAgent:
    """
    Coordinator Agent that calls the Coordinator Service to merge results.
    Does not call the LLM directly; acts as an orchestration node interface.
    """
    def __init__(self):
        self.service = ValidationCoordinatorService()

    def coordinate(
        self, 
        unique_evidence: List[Dict[str, Any]],
        credibility_scores: Dict[str, Any],
        conflicts: List[Dict[str, Any]],
        confidence_scores: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        log.info(f"ValidationCoordinatorAgent started. Merging results.")
        start_time = time.time()
        
        try:
            result = self.service.merge_validation_results(
                unique_evidence,
                credibility_scores,
                conflicts,
                confidence_scores
            )
            
            duration = time.time() - start_time
            log.info(f"ValidationCoordinatorAgent completed in {duration:.4f}s.")
            log.info(f"Validation Summary: {result['validation_summary']}")
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            log.error(f"ValidationCoordinatorAgent failed after {duration:.4f}s: {e}")
            return {
                "validated_evidence": unique_evidence,
                "discarded_evidence": [],
                "validation_report": {"error": str(e)},
                "validation_summary": "Validation failed during coordination."
            }
