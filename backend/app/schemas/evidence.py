from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class EvidenceItem(BaseModel):
    """
    Standardized schema for raw evidence collected from tools.
    Preserves all metadata. Does NOT validate or deduplicate.
    """
    id: str = Field(description="Unique identifier for the evidence")
    source: str = Field(description="Source of the evidence (e.g. Wikipedia)")
    tool: str = Field(description="The tool that generated this evidence")
    title: str = Field(description="Title of the article or page")
    content: str = Field(description="Raw content")
    summary: str = Field(description="Summary if available", default="")
    url: str = Field(description="URL to the source")
    authors: List[str] = Field(default_factory=list)
    published_date: str = Field(default="")
    retrieved_at: str = Field(description="Timestamp of collection")
    document_type: str = Field(description="Type of document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Any additional tool-specific metadata")
