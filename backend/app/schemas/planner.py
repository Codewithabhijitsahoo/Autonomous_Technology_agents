from pydantic import BaseModel, Field
from typing import List

class ResearchPlanSchema(BaseModel):
    """
    Structured Pydantic schema for the Planner Agent's output.
    Ensures that the Gemini response strictly adheres to this structure.
    """
    domain: str = Field(description="The domain classification of the request (e.g. Technology, Science, Finance).")
    complexity: str = Field(description="The complexity level: Low, Medium, or High.")
    keywords: List[str] = Field(description="Important keywords extracted from the user's query.")
    tasks: List[str] = Field(description="Step-by-step actionable research tasks to complete the research.")
    recommended_tools: List[str] = Field(description="List of tools recommended for this research from the allowed toolset.")
