import time
from typing import List, Dict, Any
from pydantic import BaseModel

class DuplicateGroup(BaseModel):
    primary_id: str
    duplicate_ids: List[str]

class DuplicateResult(BaseModel):
    duplicate_groups: List[DuplicateGroup]

class DuplicateService:
    def process_duplicates(self, raw_evidence: List[Dict[str, Any]], llm_output: DuplicateResult) -> Dict[str, Any]:
        """
        Processes LLM output to separate unique evidence from duplicates.
        """
        all_duplicates = set()
        if llm_output:
            for group in llm_output.duplicate_groups:
                all_duplicates.update(group.duplicate_ids)
            
        unique_evidence = [item for item in raw_evidence if item.get("id") not in all_duplicates]
        
        return {
            "unique_evidence": unique_evidence,
            "duplicate_groups": [g.model_dump() for g in llm_output.duplicate_groups] if llm_output else [],
            "removed_duplicates": list(all_duplicates)
        }
