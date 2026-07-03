from pydantic import BaseModel, Field
from typing import List, Optional

class ValidatedEvidenceItem(BaseModel):
    """
    Standardized schema for evidence AFTER validation via Gemini.
    """
    source: str = Field(description="The source platform of the evidence")
    title: str = Field(description="The title of the article or page")
    content: str = Field(description="The evidence content")
    url: str = Field(description="URL to the source")
    credibility_score: int = Field(ge=0, le=100, description="Heuristic credibility score (0-100)")
    confidence_score: int = Field(ge=0, le=100, description="Semantic confidence score assigned by Gemini (0-100)")
    supported_by: List[str] = Field(default_factory=list, description="URLs of sources supporting this claim")
    conflicts_with: List[str] = Field(default_factory=list, description="URLs of sources conflicting with this claim")
    is_duplicate: bool = Field(default=False, description="True if this is semantically identical to another piece of evidence")
    is_valid: bool = Field(default=True, description="True if this evidence should be kept for final report generation")
    reason: str = Field(description="Reason for validity, conflict, or rejection")

class EvidenceAnalysisResult(BaseModel):
    """
    Structured output from Gemini for semantic comparison and confidence scoring.
    """
    evaluated_items: List[ValidatedEvidenceItem]

class ValidationReport(BaseModel):
    """
    Structured validation statistics report.
    """
    total_collected: int
    total_validated: int
    total_duplicates: int
    total_conflicts: int
    total_discarded: int
    average_confidence: float
