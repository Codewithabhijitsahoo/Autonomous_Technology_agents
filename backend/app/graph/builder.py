from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from app.graph.state import GraphState
from app.graph.nodes import (
    query_understanding_node,
    intent_router_node,
    casual_chat_node,
    knowledge_answer_node,
    hypothesis_generation_node,
    planner_node, 
    task_splitter_node, 
    tool_router_node, 
    parallel_research_tools_node, 
    evidence_collector_node,
    reference_manager_node,
    fusion_grounding_node,
    duplicate_detection_node,
    source_credibility_node,
    conflict_detection_node,
    confidence_scoring_node,
    validation_coordinator_node,
    knowledge_synthesis_node,
    insight_generation_node,
    report_writer_node,
    response_relevance_node,
    review_agent_node,
    citation_formatter_node
)
from app.utils.logger import log

def route_intent(state: GraphState) -> str:
    mode = state.get("mode", "deep_research")
    if mode == "casual_chat":
        log.info("Routing to Casual Chat.")
        return "casual_chat_node"
    elif mode == "knowledge_answer":
        log.info("Routing to Knowledge Answer.")
        return "knowledge_answer_node"
    else:
        log.info("Routing to Deep Research.")
        return "hypothesis_generation_node"

def route_relevance(state: GraphState) -> str:
    # Fast-path: Never trigger partial regeneration loop to save time
    return "review_agent_node"

def build_graph():
    log.info("Building LangGraph V3 workflow (Intent Routed)...")
    
    workflow = StateGraph(GraphState)
    
    # 1. Routing & Understanding
    workflow.add_node("query_understanding_node", query_understanding_node)
    workflow.add_node("intent_router_node", intent_router_node)
    workflow.add_node("casual_chat_node", casual_chat_node)
    workflow.add_node("knowledge_answer_node", knowledge_answer_node)
    
    # 2. Hypothesis & Planning
    workflow.add_node("hypothesis_generation_node", hypothesis_generation_node)
    workflow.add_node("planner_node", planner_node)
    workflow.add_node("task_splitter_node", task_splitter_node)
    workflow.add_node("tool_router_node", tool_router_node)
    workflow.add_node("parallel_research_tools_node", parallel_research_tools_node)
    
    # 3. Evidence & Grounding
    workflow.add_node("evidence_collector_node", evidence_collector_node)
    workflow.add_node("reference_manager_node", reference_manager_node)
    workflow.add_node("fusion_grounding_node", fusion_grounding_node)
    
    # 4. Validation Pipeline
    workflow.add_node("duplicate_detection_node", duplicate_detection_node)
    workflow.add_node("source_credibility_node", source_credibility_node)
    workflow.add_node("conflict_detection_node", conflict_detection_node)
    workflow.add_node("confidence_scoring_node", confidence_scoring_node)
    workflow.add_node("validation_coordinator_node", validation_coordinator_node)
    
    # 5. Synthesis & Reporting
    workflow.add_node("knowledge_synthesis_node", knowledge_synthesis_node)
    workflow.add_node("insight_generation_node", insight_generation_node)
    workflow.add_node("report_writer_node", report_writer_node)
    
    # 6. Quality & Formatting
    workflow.add_node("response_relevance_node", response_relevance_node)
    workflow.add_node("review_agent_node", review_agent_node)
    workflow.add_node("citation_formatter_node", citation_formatter_node)
    
    # --- EDGE WIRING ---
    workflow.add_edge(START, "query_understanding_node")
    workflow.add_edge("query_understanding_node", "intent_router_node")
    
    # Conditional Intent Routing
    workflow.add_conditional_edges(
        "intent_router_node",
        route_intent,
        {
            "casual_chat_node": "casual_chat_node",
            "knowledge_answer_node": "knowledge_answer_node",
            "hypothesis_generation_node": "hypothesis_generation_node"
        }
    )
    
    # Fast paths terminate early
    workflow.add_edge("casual_chat_node", END)
    workflow.add_edge("knowledge_answer_node", END)
    
    # Deep Research Path
    workflow.add_edge("hypothesis_generation_node", "planner_node")
    
    workflow.add_edge("planner_node", "task_splitter_node")
    workflow.add_edge("task_splitter_node", "tool_router_node")
    workflow.add_edge("tool_router_node", "parallel_research_tools_node")
    workflow.add_edge("parallel_research_tools_node", "evidence_collector_node")
    
    workflow.add_edge("evidence_collector_node", "reference_manager_node")
    workflow.add_edge("reference_manager_node", "fusion_grounding_node")
    
    # FAST PATH: Skip duplicate_detection, credibility, conflict, and validation nodes
    workflow.add_edge("fusion_grounding_node", "knowledge_synthesis_node")
    
    workflow.add_edge("knowledge_synthesis_node", "insight_generation_node")
    workflow.add_edge("insight_generation_node", "report_writer_node")
    
    workflow.add_edge("report_writer_node", "response_relevance_node")
    
    # Fast path relevance routing (no loops)
    workflow.add_edge("response_relevance_node", "review_agent_node")
    
    workflow.add_edge("review_agent_node", "citation_formatter_node")
    workflow.add_edge("citation_formatter_node", END)
    
    memory = MemorySaver()
    compiled = workflow.compile(checkpointer=memory)
    log.info("LangGraph V3 compilation successful (with MemorySaver Checkpoints).")
    return compiled, memory

graph, memory_saver = build_graph()
