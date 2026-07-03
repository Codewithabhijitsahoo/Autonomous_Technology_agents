from pydantic import BaseModel, Field
from typing import List

class TopicSummary(BaseModel):
    topic: str = Field(description="Name of the topic")
    summary: str = Field(description="Comprehensive summary of the topic")

class Entity(BaseModel):
    name: str = Field(description="Entity name")
    type: str = Field(description="Type (e.g. Person, Org, Tech)")
    description: str = Field(description="Brief description of the entity")

class Fact(BaseModel):
    claim: str = Field(description="The validated claim or fact")
    sources: List[str] = Field(description="List of supporting source URLs")

class TimelineEvent(BaseModel):
    date: str = Field(description="Date or time period")
    event: str = Field(description="Description of the event")

class Relationship(BaseModel):
    source: str = Field(description="Source entity or concept")
    target: str = Field(description="Target entity or concept")
    relation: str = Field(description="How they relate (e.g. 'created_by', 'caused', 'depends_on')")

class KnowledgeGraphNode(BaseModel):
    id: str = Field(description="Unique node identifier")
    label: str = Field(description="Display label for the node")

class KnowledgeGraphEdge(BaseModel):
    source: str = Field(description="ID of the source node")
    target: str = Field(description="ID of the target node")
    relationship: str = Field(description="Relationship label")

class KnowledgeGraph(BaseModel):
    nodes: List[KnowledgeGraphNode] = Field(default_factory=list)
    edges: List[KnowledgeGraphEdge] = Field(default_factory=list)

class StructuredKnowledge(BaseModel):
    """
    Comprehensive structured knowledge synthesized from validated evidence.
    """
    executive_summary: str = Field(default="", description="High-level executive summary draft")
    topic_summaries: List[TopicSummary] = Field(default_factory=list)
    entities: List[Entity] = Field(default_factory=list)
    facts: List[Fact] = Field(default_factory=list)
    timelines: List[TimelineEvent] = Field(default_factory=list)
    relationships: List[Relationship] = Field(default_factory=list)
    statistics: List[str] = Field(default_factory=list, description="Important numerical statistics or data points")
    terminology: List[str] = Field(default_factory=list, description="Technical terms or jargon extracted")
    knowledge_graph: KnowledgeGraph = Field(default_factory=lambda: KnowledgeGraph(nodes=[], edges=[]))
