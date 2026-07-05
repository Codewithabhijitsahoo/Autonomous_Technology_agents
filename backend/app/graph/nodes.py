import time
import asyncio
from typing import Any
from app.graph.state import GraphState
from app.services.gemini_service import GeminiService
from app.utils.logger import log

from app.agents.planner_agent import PlannerAgent
from app.services.research_orchestrator import ResearchOrchestrator
from app.agents.evidence_collector_agent import EvidenceCollectorAgent
from app.agents.duplicate_detection_agent import DuplicateDetectionAgent
from app.agents.source_credibility_agent import SourceCredibilityAgent
from app.agents.conflict_detection_agent import ConflictDetectionAgent
from app.agents.confidence_scoring_agent import ConfidenceScoringAgent
from app.agents.validation_coordinator_agent import ValidationCoordinatorAgent
from app.agents.knowledge_synthesis_agent import KnowledgeSynthesisAgent
from app.agents.insight_agent import InsightGenerationAgent
from app.agents.review_agent import ReviewAgent
from app.agents.report_writer_agent import ReportWriterAgent

# New V2 Agents
from app.agents.query_understanding_agent import QueryUnderstandingAgent
from app.agents.hypothesis_generation_agent import HypothesisGenerationAgent
from app.agents.fusion_grounding_agent import FusionGroundingAgent
from app.agents.response_relevance_agent import ResponseRelevanceAgent

# New V3 Agents
from app.agents.reference_manager_agent import ReferenceManagerAgent
from app.agents.citation_formatter_agent import CitationFormatterAgent

# New V4 Routing Agents
from app.agents.intent_router_agent import IntentRouterAgent
from app.services.research_decision_service import ResearchDecisionService

gemini_service = GeminiService()
query_agent = QueryUnderstandingAgent(gemini_service=gemini_service)
hypo_agent = HypothesisGenerationAgent(gemini_service=gemini_service)
fusion_agent = FusionGroundingAgent(gemini_service=gemini_service)
relevance_agent = ResponseRelevanceAgent(gemini_service=gemini_service)

ref_manager_agent = ReferenceManagerAgent()
citation_agent = CitationFormatterAgent(gemini_service=gemini_service)

intent_router_agent = IntentRouterAgent()
decision_service = ResearchDecisionService()

planner_agent = PlannerAgent(gemini_service=gemini_service)
orchestrator = ResearchOrchestrator()
evidence_collector_agent = EvidenceCollectorAgent()

dup_agent = DuplicateDetectionAgent(gemini_service=gemini_service)
cred_agent = SourceCredibilityAgent(gemini_service=gemini_service)
conf_agent = ConflictDetectionAgent(gemini_service=gemini_service)
score_agent = ConfidenceScoringAgent(gemini_service=gemini_service)
coord_agent = ValidationCoordinatorAgent()
knowledge_agent = KnowledgeSynthesisAgent(gemini_service=gemini_service)
insight_agent = InsightGenerationAgent(gemini_service=gemini_service)
report_writer_agent = ReportWriterAgent(gemini_service=gemini_service)
review_agent = ReviewAgent(gemini_service=gemini_service)


async def query_understanding_node(state: GraphState) -> GraphState:
    query = state.get("query", "")
    metadata = state.get("metadata", {})
    if "start_time" not in metadata:
        metadata["start_time"] = time.time()
        
    try:
        sq = await query_agent.understand_query(query)
        return {"structured_query": sq, "complexity": sq.get("complexity", "Simple"), "metadata": metadata, "steps": ["query_understanding_node"]}
    except Exception as e:
        return {"errors": [f"query_understanding_node: {str(e)}"], "metadata": metadata}

async def hypothesis_generation_node(state: GraphState) -> GraphState:
    try:
        hypo = await hypo_agent.generate_hypothesis(state.get("structured_query", {}))
        return {"hypothesis_draft": hypo, "steps": ["hypothesis_generation_node"]}
    except Exception as e:
        return {"errors": [f"hypothesis_generation_node: {str(e)}"]}

async def planner_node(state: GraphState) -> GraphState:
    original_query = state.get("query", "")
    structured_query = state.get("structured_query", {})
    hypothesis = state.get("hypothesis_draft", {})
    # TASK 1: Reduce Planner Prompt Size (<1000 tokens)
    # Send only minimal required information, not full JSON or hypothesis details.
    rich_query = f"Original Query: {original_query}\nIntent: {structured_query.get('intent', 'deep_research')}\nComplexity: {state.get('complexity', 'Simple')}\nKeywords: {', '.join(structured_query.get('keywords', []))}"
    
    try:
        plan = await planner_agent.generate_plan(rich_query)
        return {"research_plan": plan.model_dump(), "tasks": plan.tasks, "keywords": plan.keywords, "domain": plan.domain, "complexity": plan.complexity, "recommended_tools": plan.recommended_tools, "steps": ["planner_node"]}
    except Exception as e:
        error_msg = str(e) or repr(e)
        return {
            "errors": [f"planner_node: {error_msg}"],
            "keywords": [original_query],
            "recommended_tools": ["Web Search", "Wikipedia"],
            "steps": ["planner_node"]
        }

async def task_splitter_node(state: GraphState) -> GraphState: 
    complexity = state.get("complexity", "Simple")
    query = state.get("query", "")
    
    if "Complex" in complexity or "Very Complex" in complexity:
        prompt = f"Split this complex research request into multiple smaller, independent research sub-tasks. Each sub-task must contain only one research objective. Return a comma-separated list of sub-tasks.\nRequest: {query}"
        try:
            res = await gemini_service.chat(prompt)
            tasks = [t.strip() for t in res.split(",") if t.strip()]
            log.info(f"Query Complexity: {complexity}. Number of Subtasks: {len(tasks)}")
            return {"tasks": tasks, "steps": ["task_splitter_node"]}
        except Exception as e:
            log.error(f"Failed to split tasks: {e}")
            
    return {"steps": ["task_splitter_node"]}
async def tool_router_node(state: GraphState) -> GraphState: return {"steps": ["tool_router_node"]}

async def parallel_research_tools_node(state: GraphState) -> GraphState:
    complexity = state.get("complexity", "Simple")
    
    if "Complex" in complexity or "Very Complex" in complexity:
        tasks = state.get("tasks", [])
        if not tasks:
            tasks = [state.get("query", "")]
            
        all_results = []
        completed = []
        failed = []
        subtask_evidence = []
        
        start_time = state.get("metadata", {}).get("start_time", time.time())
        budget = 180.0
        
        for task in tasks:
            if time.time() - start_time > budget - 30:
                log.warning("Execution budget nearly exhausted. Stopping new tasks.")
                break
                
            try:
                plan = await planner_agent.generate_plan(task)
                res = await orchestrator.execute_plan(task, plan.recommended_tools)
                normalized, stats = await evidence_collector_agent.collect_and_organize(res["research_results"])
                # TASK 11: Search Quality Validation (Retry once if no results)
                if stats['total'] == 0:
                    log.warning(f"Subtask '{task}' returned 0 results. Retrying with official sources and broader keywords.")
                    fallback_plan = await planner_agent.generate_plan(f"Retry search for: {task}. Use ONLY highly official sources, company websites, GitHub, or trusted news.")
                    res = await orchestrator.execute_plan(task, fallback_plan.recommended_tools)
                    normalized, stats = await evidence_collector_agent.collect_and_organize(res["research_results"])

                subtask_evidence.append({
                    "task": task,
                    "evidence": normalized
                })
                completed.extend(res["completed_tools"])
                failed.extend(res["failed_tools"])
                log.info(f"Subtask '{task}' completed. Evidence Count: {stats['total']}")
                
            except Exception as e:
                failed.append(f"{task}: {e}")
                
        return {
            "subtask_evidence": subtask_evidence,
            "completed_tools": completed,
            "failed_tools": failed,
            "steps": ["parallel_research_tools_node"]
        }
    else:
        keywords = state.get("keywords", [])
        search_query = " ".join(keywords) if keywords else state.get("query", "")
        recommended_tools = state.get("recommended_tools", [])
        try:
            result = await orchestrator.execute_plan(search_query, recommended_tools)
            return {"research_results": result["research_results"], "completed_tools": result["completed_tools"], "failed_tools": result["failed_tools"], "steps": ["parallel_research_tools_node"]}
        except Exception as e:
            return {"errors": [f"parallel_research_tools_node: {str(e)}"]}

async def evidence_collector_node(state: GraphState) -> GraphState:
    complexity = state.get("complexity", "Simple")
    if "Complex" in complexity or "Very Complex" in complexity:
        subtasks = state.get("subtask_evidence", [])
        flat_evidence = []
        for st in subtasks:
            flat_evidence.extend(st["evidence"])
        log.info(f"Flattened {len(flat_evidence)} evidence items from subtasks for compatibility.")
        return {"raw_evidence": flat_evidence, "evidence_count": len(flat_evidence), "steps": ["evidence_collector_node"]}
    else:
        raw_results = state.get("research_results", [])
        try:
            normalized, stats = await evidence_collector_agent.collect_and_organize(raw_results)
            return {"raw_evidence": normalized, "evidence_count": stats["total"], "tool_statistics": stats, "steps": ["evidence_collector_node"]}
        except Exception as e:
            return {"errors": [f"evidence_collector_node: {str(e)}"]}

async def reference_manager_node(state: GraphState) -> GraphState:
    try:
        res = await ref_manager_agent.process_references(state.get("raw_evidence", []))
        return {
            "reference_map": res["reference_map"],
            "evidence_traceability": res["traceable_evidence"],
            "citations": res["citations"],
            "steps": ["reference_manager_node"]
        }
    except Exception as e:
        return {"errors": [f"reference_manager_node: {str(e)}"]}

async def fusion_grounding_node(state: GraphState) -> GraphState:
    try:
        gd = await fusion_agent.fuse(state.get("hypothesis_draft", {}), state.get("evidence_traceability", []))
        return {"grounded_draft": gd, "steps": ["fusion_grounding_node"]}
    except Exception as e:
        return {"errors": [f"fusion_grounding_node: {str(e)}"]}

async def duplicate_detection_node(state: GraphState) -> GraphState:
    try:
        gd = state.get("grounded_draft", {})
        evidence_item = {"title": "Grounded Draft", "content": gd.get("enhanced_draft_content", ""), "source": "Fusion Agent"}
        res = await dup_agent.detect([evidence_item])
        return {"unique_evidence": res["unique_evidence"], "duplicate_groups": res["duplicate_groups"], "steps": ["duplicate_detection_node"]}
    except Exception as e:
        return {"errors": [f"duplicate_detection_node: {str(e)}"]}

async def intent_router_node(state: GraphState) -> GraphState:
    # TASK 2: Intent is already determined in query_understanding_node
    # We no longer need to call IntentRouterAgent (Gemini)
    sq = state.get("structured_query", {})
    if "mode" in sq:
        mode = sq["mode"]
    else:
        # Fallback if fast path wasn't activated but mode exists somehow
        mode = state.get("mode", sq.get("intent", "deep_research"))
        
    return {"mode": mode, "steps": ["intent_router_node"]}

async def casual_chat_node(state: GraphState) -> GraphState:
    # TASK 4 & 5: Static Casual Responses
    sq = state.get("structured_query", {})
    if sq.get("fast_path_activated") and sq.get("response"):
        log.info("Returning static fast-path casual chat response.")
        return {"response": sq.get("response"), "steps": ["casual_chat_node"]}
        
    log.info("No static response found, falling back to Gemini casual chat.")
    prompt = f"User said: {state.get('query')}. Respond casually and concisely."
    try:
        response = await gemini_service.chat(prompt, task_type="general", complexity="Simple")
        return {"response": response, "steps": ["casual_chat_node"]}
    except Exception as e:
        return {"errors": [f"casual_chat_node: {str(e)}"]}

async def source_credibility_node(state: GraphState) -> GraphState:
    try:
        scores = await cred_agent.analyze(state.get("unique_evidence", []))
        return {"credibility_scores": scores, "steps": ["source_credibility_node"]}
    except Exception as e:
        return {"errors": [f"source_credibility_node: {str(e)}"]}

async def conflict_detection_node(state: GraphState) -> GraphState:
    try:
        conflicts = await conf_agent.detect(state.get("unique_evidence", []))
        return {"conflicts": conflicts, "steps": ["conflict_detection_node"]}
    except Exception as e:
        return {"errors": [f"conflict_detection_node: {str(e)}"]}

async def confidence_scoring_node(state: GraphState) -> GraphState:
    try:
        scores = await score_agent.score(state.get("unique_evidence", []), state.get("credibility_scores", {}), state.get("conflicts", []))
        return {"confidence_scores": scores, "steps": ["confidence_scoring_node"]}
    except Exception as e:
        return {"errors": [f"confidence_scoring_node: {str(e)}"]}

async def validation_coordinator_node(state: GraphState) -> GraphState:
    try:
        res = coord_agent.coordinate(state.get("unique_evidence", []), state.get("credibility_scores", {}), state.get("conflicts", []), state.get("confidence_scores", {}))
        return {"validated_evidence": res.get("validated_evidence", []), "discarded_evidence": res.get("discarded_evidence", []), "validation_report": res.get("validation_report", {}), "validation_summary": res.get("validation_summary", ""), "steps": ["validation_coordinator_node"]}
    except Exception as e:
        return {"errors": [f"validation_coordinator_node: {str(e)}"]}

async def knowledge_synthesis_node(state: GraphState) -> GraphState:
    try:
        if state.get("evidence_count", 0) == 0:
            log.warning("Evidence == 0. Skipping Knowledge Synthesis.")
            return {"knowledge": {}, "steps": ["knowledge_synthesis_node"]}
            
        complexity = state.get("complexity", "Simple")
        if ("Complex" in complexity or "Very Complex" in complexity) and state.get("subtask_evidence"):
            start_time = time.time()
            knowledge_dict = await knowledge_agent.hierarchical_synthesize(state.get("subtask_evidence"))
            log.info(f"Hierarchical Merge Time: {time.time() - start_time:.2f}s")
        else:
            evidence = state.get("validated_evidence", [])
            if not evidence:
                evidence = state.get("evidence_traceability", [])
            query = state.get("query", "")
            references = state.get("reference_map", {})
            knowledge_dict = await knowledge_agent.synthesize(evidence, query, references)
            
        return {
            "knowledge": knowledge_dict,
            "executive_summary": knowledge_dict.get("executive_summary", ""),
            "topic_summaries": knowledge_dict.get("topic_summaries", []),
            "entities": knowledge_dict.get("entities", []),
            "facts": knowledge_dict.get("facts", []),
            "timelines": knowledge_dict.get("timelines", []),
            "relationships": knowledge_dict.get("relationships", []),
            "statistics": knowledge_dict.get("statistics", []),
            "terminology": knowledge_dict.get("terminology", []),
            "knowledge_graph": knowledge_dict.get("knowledge_graph", {}),
            "steps": ["knowledge_synthesis_node"]
        }
    except Exception as e:
        return {"errors": [f"knowledge_synthesis_node: {str(e)}"]}

async def insight_generation_node(state: GraphState) -> GraphState:
    try:
        evidence_count = state.get("evidence_count", 0)
        if evidence_count == 0:
            return {"insights": [], "steps": ["insight_generation_node"]}
        if evidence_count < 3:
            log.info("Evidence < 3. Skipping Insight Generation to save costs.")
            return {"insights": [], "steps": ["insight_generation_node"]}
            
        res = await insight_agent.generate_insights(state.get("knowledge", {}))
        return {
            "insights": res.get("insights", []),
            "trend_analysis": res.get("trend_analysis", []),
            "comparisons": res.get("comparisons", []),
            "opportunities": res.get("opportunities", []),
            "risks": res.get("risks", []),
            "limitations": res.get("limitations", []),
            "future_research": res.get("future_research", []),
            "strategic_takeaways": res.get("strategic_takeaways", []),
            "steps": ["insight_generation_node"]
        }
    except Exception as e:
        return {"errors": [f"insight_generation_node: {str(e)}"]}

async def report_writer_node(state: GraphState) -> GraphState:
    log.info("Node execution started: report_writer_node")
    start_time = time.time()
    try:
        if state.get("evidence_count", 0) == 0:
            return {"final_report": "No verified evidence could be collected from the available sources.", "steps": ["report_writer_node"], "execution_time": time.time() - start_time}
            
        report = await report_writer_agent.write_report(
            query=state.get("query", ""),
            knowledge=state.get("knowledge", {}),
            insights=state.get("insights", [])
        )
        return {
            "final_report": report,
            "steps": ["report_writer_node"],
            "execution_time": time.time() - start_time
        }
    except Exception as e:
        log.error(f"Error in report_writer_node: {e}")
        return {"errors": [f"report_writer_node: {str(e)}"]}

async def response_relevance_node(state: GraphState) -> GraphState:
    try:
        if state.get("evidence_count", 0) == 0:
            return {"steps": ["response_relevance_node"]}
            
        metrics = await relevance_agent.check_relevance(
            state.get("query", ""),
            state.get("structured_query", {}),
            state.get("final_report", "")
        )
        return {"relevance_metrics": metrics, "steps": ["response_relevance_node"]}
    except Exception as e:
        return {"errors": [f"response_relevance_node: {str(e)}"]}

async def review_agent_node(state: GraphState) -> GraphState:
    log.info("Node execution started: review_agent_node")
    start_time = time.time()
    try:
        report = state.get("final_report", "")
        if state.get("evidence_count", 0) == 0 or len(report) < 200:
            log.info("Skipping review for fallback/empty report.")
            return {"reviewed_report": report, "quality_scores": {"overall_score": 100}, "steps": ["review_agent_node"]}
            
        query = state.get("query", "")
        reference_map = state.get("reference_map", {})
        
        res = await review_agent.review(report, query, reference_map)
        
        return {
            "reviewed_report": res.get("reviewed_report", report),
            "quality_scores": res.get("quality_scores", {}),
            "quality_report": res.get("quality_report", {}),
            "review_summary": res.get("review_summary", ""),
            "improvements": res.get("improvements", []),
            "issues_found": res.get("issues_found", []),
            "steps": ["review_agent_node"],
            "execution_time": time.time() - start_time
        }
    except Exception as e:
        log.error(f"Error in review_agent_node: {e}")
        return {
            "errors": [f"review_agent_node: {str(e)}"],
            "reviewed_report": state.get("final_report", ""),
            "steps": ["review_agent_node"]
        }

async def citation_formatter_node(state: GraphState) -> GraphState:
    try:
        res = await citation_agent.format_citations(state.get("reviewed_report", state.get("final_report", "")), state.get("reference_map", {}))
        return {
            "final_report": res["formatted_report"],
            "citations": res["citations"],
            "steps": ["citation_formatter_node"]
        }
    except Exception as e:
        return {"errors": [f"citation_formatter_node: {str(e)}"]}

async def intent_router_node(state: GraphState) -> GraphState:
    try:
        structured_query = state.get("structured_query", {})
        intent_data = intent_router_agent.route_intent(structured_query)
        return {
            "intent": intent_data["intent"],
            "research_score": intent_data["research_score"],
            "mode": intent_data["mode"],
            "steps": ["intent_router_node"]
        }
    except Exception as e:
        return {"errors": [f"intent_router_node: {str(e)}"]}

async def casual_chat_node(state: GraphState) -> GraphState:
    try:
        response = await gemini_service.chat(f"You are a helpful and friendly AI assistant. The user just said: '{state.get('query', '')}'. Reply directly to the user in a short, conversational, and friendly manner. Do not provide a list of ways to reply.")
        return {"final_report": response, "steps": ["casual_chat_node"]}
    except Exception as e:
        return {"errors": [f"casual_chat_node: {str(e)}"]}

async def knowledge_answer_node(state: GraphState) -> GraphState:
    try:
        response = await gemini_service.chat(f"Provide a comprehensive, factual answer to this question based on your internal knowledge: {state.get('query', '')}")
        return {"final_report": response, "steps": ["knowledge_answer_node"]}
    except Exception as e:
        return {"errors": [f"knowledge_answer_node: {str(e)}"]}

