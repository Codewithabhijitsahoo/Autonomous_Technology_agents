import time
import json
from typing import List, Dict, Any, Tuple
from app.services.gemini_service import GeminiService
from app.services.validation_service import ValidationService
from app.prompts.validator_prompt import VALIDATOR_SYSTEM_PROMPT
from app.schemas.validator import EvidenceAnalysisResult, ValidationReport, ValidatedEvidenceItem
from app.utils.logger import log

class ValidatorAgent:
    """
    The Validator Agent orchestrates the evidence validation pipeline.
    It reads raw evidence, applies heuristic rules, and uses Gemini for complex semantic comparison.
    """
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.validation_service = ValidationService()

    async def validate_evidence(self, raw_evidence: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any], List[str]]:
        """
        Validates evidence. Returns (validated_evidence_dicts, validation_report_dict, conflicts_list)
        """
        log.info(f"ValidatorAgent starting validation for {len(raw_evidence)} items.")
        start_time = time.time()
        
        if not raw_evidence:
            log.warning("No evidence to validate.")
            empty_report = self.validation_service.generate_report([]).model_dump()
            return [], empty_report, []
        
        try:
            # Step 1: Programmatic heuristic ranking (Layer 2)
            evidence_with_baseline = self.validation_service.assign_baseline_credibility(raw_evidence)
            
            # Step 2: Semantic evaluation via Gemini (Duplicate, Conflict, Confidence, Freshness)
            evidence_json = json.dumps(evidence_with_baseline, indent=2)
            prompt = f"Please evaluate the following evidence items and return the structured validation list:\n\n{evidence_json}"
            
            # Call Gemini with structured output
            analysis_result: EvidenceAnalysisResult = await self.gemini_service.structured_chat(
                prompt=prompt,
                schema=EvidenceAnalysisResult,
                system_prompt=VALIDATOR_SYSTEM_PROMPT
            )
            
            validated_items = analysis_result.evaluated_items
            
            # Step 3: Generate statistics report
            report = self.validation_service.generate_report(validated_items)
            
            # Extract pure conflicts for state tracking
            conflicts = []
            for item in validated_items:
                if item.conflicts_with:
                    conflicts.append(f"Conflict found in {item.source} ({item.title}) with {item.conflicts_with}")
                    
            duration = time.time() - start_time
            log.info(f"ValidatorAgent finished successfully in {duration:.4f}s")
            log.info(f"Validation Report: {report.model_dump()}")
            
            # Return serialized versions for the graph state
            validated_dicts = [item.model_dump() for item in validated_items]
            
            return validated_dicts, report.model_dump(), conflicts
            
        except Exception as e:
            duration = time.time() - start_time
            log.error(f"ValidatorAgent encountered an error after {duration:.4f}s: {e}")
            raise e
