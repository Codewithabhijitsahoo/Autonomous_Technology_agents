import time
from typing import List, Dict, Any, Tuple
from app.services.evidence_service import EvidenceService
from app.utils.logger import log

class EvidenceCollectorAgent:
    """
    Agent that acts as a pure collector and normalizer.
    Receives outputs from all tools and standardizes them.
    Never removes, validates, or deduplicates.
    """
    def __init__(self):
        self.evidence_service = EvidenceService()

    async def collect_and_organize(self, raw_evidence: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        log.info(f"EvidenceCollectorAgent starting collection of {len(raw_evidence)} raw items.")
        start_time = time.time()
        
        try:
            normalized = self.evidence_service.normalize(raw_evidence)
            stats = self.evidence_service.generate_statistics(normalized)
            
            duration = time.time() - start_time
            log.info(f"Collection completed in {duration:.4f}s. Total collected: {stats['total']}")
            
            # Log the required statistics
            log.info("Tool statistics:")
            for k, v in stats.get("counts_by_source", {}).items():
                log.info(f"- {k}: {v}")
            log.info(f"Total evidence: {stats['total']}")
            
            return normalized, stats
            
        except Exception as e:
            duration = time.time() - start_time
            log.error(f"EvidenceCollectorAgent encountered an error after {duration:.4f}s: {e}")
            raise e
