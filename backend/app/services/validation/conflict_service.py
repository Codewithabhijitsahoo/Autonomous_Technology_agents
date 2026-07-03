from typing import List, Dict, Any
from pydantic import BaseModel

class Conflict(BaseModel):
    conflict_reason: str
    conflicting_evidence_ids: List[str]

class ConflictResult(BaseModel):
    conflicts: List[Conflict]

class ConflictService:
    def process_conflicts(self, llm_output: ConflictResult) -> List[Dict[str, Any]]:
        """
        Processes conflicts from LLM output.
        """
        if not llm_output:
            return []
        return [c.model_dump() for c in llm_output.conflicts]
