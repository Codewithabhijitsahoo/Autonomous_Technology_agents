import operator
from typing import TypedDict, List, Dict, Any, Optional, Annotated

class GraphState(TypedDict, total=False):
    # Base
    query: str
    messages: Annotated[List[Dict[str, Any]], operator.add]
    response: Optional[str]
    steps: Annotated[List[str], operator.add]
    metadata: Dict[str, Any]
    errors: Annotated[List[str], operator.add]
    sources: Annotated[List[str], operator.add]
    execution_time: float
    
    # V2 Architecture Additions
    structured_query: Dict[str, Any]
    hypothesis_draft: Dict[str, Any]
    grounded_draft: Dict[str, Any]
    relevance_metrics: Dict[str, Any]
    
    # V3 Traceability Additions
    reference_map: Dict[str, Any]
    citations: List[Dict[str, Any]]
    evidence_traceability: List[Dict[str, Any]]
    
    # V4 Intent Routing Additions
    intent: str
    research_score: int
    mode: str
    
    # Planner
    research_plan: Optional[Dict[str, Any]]
    tasks: List[str]
    keywords: List[str]
    domain: str
    complexity: str
    recommended_tools: List[str]
    
    # Orchestrator
    research_results: Annotated[List[Dict[str, Any]], operator.add]
    completed_tools: Annotated[List[str], operator.add]
    failed_tools: Annotated[List[str], operator.add]
    
    # Evidence Collector
    raw_evidence: Annotated[List[Dict[str, Any]], operator.add]
    evidence_count: int
    tool_statistics: Dict[str, Any]
    collection_metadata: Dict[str, Any]
    
    # Modular Validation Pipeline
    unique_evidence: List[Dict[str, Any]]
    duplicate_groups: List[Dict[str, Any]]
    credibility_scores: Dict[str, Any]
    conflicts: List[Dict[str, Any]]
    confidence_scores: Dict[str, Any]
    validated_evidence: List[Dict[str, Any]]
    discarded_evidence: List[Dict[str, Any]]
    validation_report: Dict[str, Any]
    validation_summary: str
    
    # Knowledge Synthesis
    knowledge: Dict[str, Any]
    executive_summary: str
    topic_summaries: List[Dict[str, Any]]
    entities: List[Dict[str, Any]]
    facts: List[Dict[str, Any]]
    timelines: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    statistics: List[str]
    terminology: List[str]
    knowledge_graph: Dict[str, Any]
    
    # Insight Generation
    insights: List[Dict[str, Any]]
    trend_analysis: List[Dict[str, Any]]
    comparisons: List[Dict[str, Any]]
    risks: List[str]
    opportunities: List[str]
    limitations: List[str]
    future_research: List[str]
    strategic_takeaways: List[str]
    
    # Report Generation (Mocked for Step 9)
    final_report: str
    
    # Review Agent (Step 9)
    reviewed_report: str
    quality_scores: Dict[str, Any]
    quality_report: Dict[str, Any]
    review_summary: str
    improvements: List[str]
    issues_found: List[Dict[str, Any]]
