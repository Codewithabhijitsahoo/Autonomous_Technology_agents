import time
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from app.services.gemini_service import GeminiService
from app.utils.logger import log

class GroundedDraftSchema(BaseModel):
    supported_statements: List[str] = Field(description="Statements from the hypothesis supported by evidence")
    unsupported_statements: List[str] = Field(description="Statements from the hypothesis contradicted or not found in evidence")
    missing_facts: List[str] = Field(description="New facts found in evidence missing from the hypothesis")
    contradictions: List[str] = Field(description="Contradictions found")
    outdated_information: List[str] = Field(description="Outdated info identified")
    enhanced_draft_content: str = Field(description="The full merged content combining hypothesis and evidence facts without making truth judgments")

class FusionGroundingAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def fuse(self, hypothesis_draft: dict, normalized_evidence: list) -> dict:
        log.info("FusionGroundingAgent starting.")
        start_time = time.time()
        try:
            prompt = f"Hypothesis Draft:\n{hypothesis_draft}\n\nEvidence:\n{normalized_evidence}"
            res: GroundedDraftSchema = await self.gemini_service.structured_chat(
                prompt=prompt,
                schema=GroundedDraftSchema,
                system_prompt="You are a Fusion/Grounding Agent. Compare the hypothesis draft with the collected evidence. Annotate supported, unsupported, missing, and contradictory facts. Produce an enhanced draft."
            )
            log.info(f"FusionGroundingAgent finished in {time.time() - start_time:.2f}s")
            return res.model_dump()
        except Exception as e:
            log.error(f"FusionGroundingAgent error: {e}")
            raise e
