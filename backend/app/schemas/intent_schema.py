from pydantic import BaseModel, Field

class IntentSchema(BaseModel):
    intent: str = Field(description="The classified intent of the user query.")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0.")
    needs_latest_info: bool = Field(description="True if the query requires up-to-date real-time information.")
    needs_multiple_sources: bool = Field(description="True if the query requires synthesizing information from multiple sources.")
    complexity: int = Field(description="Estimated complexity of the query from 1 to 10.")
    topics_count: int = Field(description="Number of distinct topics in the query.")
