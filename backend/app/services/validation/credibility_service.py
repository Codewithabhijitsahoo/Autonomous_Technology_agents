from typing import List, Dict, Any
from pydantic import BaseModel

class CredibilityScore(BaseModel):
    evidence_id: str
    credibility_score: int
    credibility_reason: str

class CredibilityResult(BaseModel):
    scores: List[CredibilityScore]

class CredibilityService:
    def process_scores(self, llm_output: CredibilityResult) -> Dict[str, Dict[str, Any]]:
        """
        Converts LLM credibility output into a fast lookup dictionary.
        Returns Dict[evidence_id, {score, reason}]
        """
        result = {}
        if llm_output:
            for score in llm_output.scores:
                result[score.evidence_id] = {
                    "score": score.credibility_score,
                    "reason": score.credibility_reason
                }
        return result
