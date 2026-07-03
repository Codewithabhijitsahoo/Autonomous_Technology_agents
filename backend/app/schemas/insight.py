from pydantic import BaseModel, Field
from typing import List

class InsightItem(BaseModel):
    title: str = Field(description="Title of the insight")
    category: str = Field(description="Category (e.g., Trend, Pattern, Cause and Effect, Comparative)")
    description: str = Field(description="Detailed description of the insight")
    confidence: int = Field(description="Confidence score (0-100)")
    supporting_evidence: List[str] = Field(description="IDs or URLs of supporting evidence")

class StructuredInsights(BaseModel):
    insights: List[InsightItem] = Field(default_factory=list, description="Array of deep insights extracted from the knowledge")
    opportunities: List[str] = Field(default_factory=list, description="Identified strategic opportunities")
    risks: List[str] = Field(default_factory=list, description="Identified risks or threats")
    limitations: List[str] = Field(default_factory=list, description="Identified limitations in the data or topic")
    future_research: List[str] = Field(default_factory=list, description="Identified research gaps or future directions")
    strategic_takeaways: List[str] = Field(default_factory=list, description="Key strategic observations and takeaways")
