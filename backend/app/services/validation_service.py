import time
from typing import List, Dict, Any
from app.schemas.validator import ValidatedEvidenceItem, ValidationReport
from app.utils.logger import log

class ValidationService:
    """
    Service for applying programmatic validation rules (Source Credibility Ranking) 
    and generating validation statistics.
    """
    
    # Layer 2: Static rule-based credibility baseline based on source types
    CREDIBILITY_MAP = {
        "Research Papers (Arxiv)": 95,
        "Wikipedia": 70,
        "News Search": 65,
        "Web Search (Tavily)": 50,
        "Web Search (DDG)": 50,
        "Unknown": 30
    }

    def assign_baseline_credibility(self, evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Assigns a baseline credibility score to evidence based on source type.
        Gemini can later adjust this based on semantic content.
        """
        for item in evidence:
            source = item.get("source", "Unknown")
            item["baseline_credibility"] = self.CREDIBILITY_MAP.get(source, 50)
        return evidence
        
    def generate_report(self, validated_items: List[ValidatedEvidenceItem]) -> ValidationReport:
        """
        Generates the final statistics report from the validated evidence list.
        """
        total = len(validated_items)
        duplicates = sum(1 for item in validated_items if item.is_duplicate)
        conflicts = sum(1 for item in validated_items if len(item.conflicts_with) > 0)
        discarded = sum(1 for item in validated_items if not item.is_valid)
        validated = total - discarded
        
        valid_items = [item for item in validated_items if item.is_valid]
        avg_confidence = sum(item.confidence_score for item in valid_items) / max(1, len(valid_items)) if valid_items else 0
        
        return ValidationReport(
            total_collected=total,
            total_validated=validated,
            total_duplicates=duplicates,
            total_conflicts=conflicts,
            total_discarded=discarded,
            average_confidence=round(avg_confidence, 2)
        )
