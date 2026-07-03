from typing import List, Dict, Any
from pydantic import BaseModel

class ConfidenceScore(BaseModel):
    evidence_id: str
    confidence_score: int
    confidence_reason: str

class ConfidenceResult(BaseModel):
    scores: List[ConfidenceScore]

class ConfidenceService:
    def process_scores(self, llm_output: ConfidenceResult) -> Dict[str, Dict[str, Any]]:
        """
        Converts LLM confidence output into a fast lookup dictionary.
        Returns Dict[evidence_id, {score, reason}]
        """
        result = {}
        if llm_output:
            for score in llm_output.scores:
                result[score.evidence_id] = {
                    "score": score.confidence_score,
                    "reason": score.confidence_reason
                }
        return result
