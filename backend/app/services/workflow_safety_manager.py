import asyncio
import time
from typing import Dict, Any
from app.config.settings import settings
from app.utils.logger import log
from app.graph.nodes import report_writer_node, review_agent_node, citation_formatter_node
from app.graph.builder import graph

class WorkflowSafetyManager:
    """
    Global Safety Manager that acts as the final protection layer.
    Ensures the workflow never hangs indefinitely and always returns a report.
    """
    def __init__(self):
        self.budget = settings.global_execution_budget
        
    async def execute_safely(self, initial_state: Dict[str, Any], thread_id: str) -> Dict[str, Any]:
        """
        Executes the LangGraph workflow wrapped in a global safety budget.
        If it times out or fails at the top level, it salvages the checkpoint state and forces report generation.
        """
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            # Run normal workflow with a hard timeout matching the safety budget
            log.info(f"WorkflowSafetyManager: Starting execution with budget of {self.budget}s")
            final_state = await asyncio.wait_for(graph.ainvoke(initial_state, config=config), timeout=self.budget)
            log.info("WorkflowSafetyManager: Normal execution completed successfully.")
            return final_state
            
        except asyncio.TimeoutError:
            log.warning(f"WorkflowSafetyManager: GLOBAL SAFETY BUDGET ({self.budget}s) EXCEEDED. Workflow stuck. Forcing recovery.")
            return await self._salvage_checkpoint(config, initial_state)
        except Exception as e:
            log.error(f"WorkflowSafetyManager: Unhandled top-level exception: {e}. Forcing recovery.")
            return await self._salvage_checkpoint(config, initial_state)
            
    async def _salvage_checkpoint(self, config: Dict[str, Any], initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recovers the latest valid state from the LangGraph Checkpointer.
        Bypasses the rest of the workflow and immediately generates the report.
        """
        # Retrieve the last saved checkpoint
        checkpoint = graph.get_state(config)
        state = checkpoint.values if checkpoint and checkpoint.values else initial_state
        
        # Determine if we have enough evidence to salvage
        evidence_count = state.get("evidence_count", 0)
        log.info(f"WorkflowSafetyManager: Checkpoint retrieved. Evidence count: {evidence_count}")
        
        # Inject emergency warning into knowledge summary to notify downstream nodes and the user
        warning_msg = "\n\n**Note: Research ended after reaching the workflow safety limit. This report contains all verified evidence collected before execution stopped.**"
        
        knowledge = state.get("knowledge", {})
        if not knowledge:
            knowledge = {"executive_summary": "System recovered from an unexpected delay."}
            
        knowledge["executive_summary"] = knowledge.get("executive_summary", "") + warning_msg
        state["knowledge"] = knowledge
        
        if evidence_count == 0:
            state["final_report"] = "Research ended unexpectedly due to system limits, and no verified evidence was collected in time. Please try a more specific or narrower query."
            return state
            
        # Force manual execution of the reporting pipeline to salvage the evidence
        try:
            if not state.get("final_report"):
                log.info("WorkflowSafetyManager: Forcing Report Writer...")
                state = await report_writer_node(state)
            else:
                log.info("WorkflowSafetyManager: Report already exists. Skipping Report Writer.")
                
            if not state.get("reviewed_report") and state.get("final_report"):
                log.info("WorkflowSafetyManager: Forcing Review Agent...")
                state = await review_agent_node(state)
            else:
                log.info("WorkflowSafetyManager: Review already exists or no report. Skipping Review Agent.")
                
            if not state.get("citations") and state.get("reviewed_report"):
                log.info("WorkflowSafetyManager: Forcing Citation Formatter...")
                state = await citation_formatter_node(state)
            else:
                log.info("WorkflowSafetyManager: Citations already exist or no reviewed report. Skipping Citation Formatter.")
                
            log.info("WorkflowSafetyManager: Emergency report generation successful.")
        except Exception as e:
            log.error(f"WorkflowSafetyManager: Emergency generation failed: {e}")
            state["final_report"] = f"A critical error prevented report generation after the safety limit was reached. Available evidence count: {evidence_count}."
            
        return state
