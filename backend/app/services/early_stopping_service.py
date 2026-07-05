from typing import List, Dict, Any, Set
from app.config.settings import settings
from app.utils.logger import log

class EarlyStoppingService:
    """
    Service responsible for evaluating whether background workflow tasks
    (like parallel search execution) can be safely cancelled based on information sufficiency.
    """
    def __init__(self):
        self.evidence_threshold = settings.early_stop_evidence_threshold
        self.high_priority_tools = set(settings.early_stop_high_priority_tools)
        
    def should_stop_search(
        self,
        collected_evidence: List[Dict[str, Any]],
        completed_tools: Set[str],
        pending_tools: Set[str],
        failed_tools: Set[str]
    ) -> bool:
        """
        Evaluates whether we should cancel pending search tasks and proceed to synthesis.
        """
        # Condition 1: Check if we have gathered enough high-quality evidence
        if len(collected_evidence) >= self.evidence_threshold:
            log.info(f"Early Stop | Reason: Sufficient verified evidence collected ({len(collected_evidence)} items).")
            return True
            
        # Condition 2: Check if all high-priority searches have completed (successfully or failed)
        remaining_tools = pending_tools
        remaining_high_priority = remaining_tools.intersection(self.high_priority_tools)
        
        if not remaining_high_priority and len(collected_evidence) > 0:
            log.info(f"Early Stop | Reason: All high-priority searches completed and base evidence gathered.")
            return True
            
        # Condition 5 & 6: Only low-value tools remaining with sufficient base evidence
        if len(collected_evidence) >= (self.evidence_threshold // 2) and all(t not in self.high_priority_tools for t in remaining_tools):
            log.info(f"Early Stop | Reason: Remaining tasks ({', '.join(remaining_tools)}) are low priority and sufficient base evidence exists.")
            return True
            
        return False
