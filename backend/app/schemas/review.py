from pydantic import BaseModel, Field
from typing import List

class QualityScores(BaseModel):
    accuracy: int = Field(description="Score for factual accuracy (0-100)")
    completeness: int = Field(description="Score for completeness (0-100)")
    evidence_coverage: int = Field(description="Score for evidence coverage (0-100)")
    readability: int = Field(description="Score for readability (0-100)")
    consistency: int = Field(description="Score for consistency (0-100)")
    professional_writing: int = Field(description="Score for professional writing (0-100)")
    overall_score: int = Field(description="Overall aggregate score (0-100)")

class Issue(BaseModel):
    issue_type: str = Field(description="E.g., Grammar, Factual, Contradiction, Missing Reference")
    description: str = Field(description="Detailed description of the issue")
    severity: str = Field(description="'minor' or 'major'")
    suggested_fix: str = Field(description="Suggested fix or actual fix applied")

class ReviewResult(BaseModel):
    reviewed_report: str = Field(description="The final auto-corrected report text")
    quality_scores: QualityScores = Field(description="Detailed quality scores")
    strengths: List[str] = Field(description="Strengths of the report")
    weaknesses: List[str] = Field(description="Weaknesses of the report")
    missing_topics: List[str] = Field(description="Topics that were missed")
    unsupported_claims: List[str] = Field(description="Claims lacking evidence")
    contradictions: List[str] = Field(description="Contradictory statements")
    formatting_problems: List[str] = Field(description="Formatting issues")
    issues_found: List[Issue] = Field(description="Detailed list of specific issues found")
    improvements_made: List[str] = Field(description="List of minor auto-corrections applied to the reviewed report")
