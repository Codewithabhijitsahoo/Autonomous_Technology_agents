import asyncio
import time
from typing import Dict, Any, List
from app.tools.web_search import search_web
from app.tools.wikipedia_search import search_wikipedia
from app.tools.arxiv_search import search_arxiv
from app.tools.news_search import search_news
from app.schemas.evidence import EvidenceItem
from app.utils.logger import log
from app.services.early_stopping_service import EarlyStoppingService

class ResearchOrchestrator:
    """
    Service responsible for orchestrating concurrent execution of research tools based on the planner's output.
    Supports failure isolation, preventing one failed tool from halting the whole graph.
    """
    def __init__(self):
        self.tool_map = {
            "Web Search": search_web,
            "Wikipedia": search_wikipedia,
            "Research Papers": search_arxiv,
            "News Search": search_news
        }
        self.early_stopping_service = EarlyStoppingService()

    async def execute_plan(self, query: str, recommended_tools: List[str]) -> Dict[str, Any]:
        """
        Executes the tools recommended by the Planner in parallel.
        """
        log.info(f"Research Orchestrator starting. Requested tools: {recommended_tools}")
        
        tasks_to_run = []
        delay_counter = 0.0
        
        # Dispatch requested tools
        for tool_name in recommended_tools:
            if tool_name in self.tool_map:
                tasks_to_run.append(self.run_tool_safely(tool_name, self.tool_map[tool_name], query, delay=delay_counter))
                # Stagger DuckDuckGo tools by 2 seconds to avoid 403 Rate Limits
                if tool_name in ["Web Search", "News Search"]:
                    delay_counter += 2.0
        
        # Fallback if the planner didn't recommend any valid tools
        if not tasks_to_run:
            log.warning("No recognized tools in recommended_tools. Defaulting to Web Search.")
            tasks_to_run.append(self.run_tool_safely("Web Search", search_web, query, delay=0.0))

        start_time = time.time()
        # Execute tools independently and concurrently
        completed_tools = set()
        failed_tools = set()
        pending_tools = set(recommended_tools)
        raw_evidence = []
        
        # Use asyncio.as_completed for early stopping evaluation
        pending_tasks = [asyncio.create_task(task) for task in tasks_to_run]
        
        while pending_tasks:
            done, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
            
            for task in done:
                try:
                    tool_name, status, data = task.result()
                    pending_tools.discard(tool_name)
                    
                    if status == "success":
                        completed_tools.add(tool_name)
                        raw_evidence.extend(data)
                    else:
                        failed_tools.add(f"{tool_name}: {data}")
                        
                except Exception as e:
                    log.error(f"Task encountered an exception: {e}")
                    
            # Evaluate Early Stopping
            if self.early_stopping_service.should_stop_search(
                collected_evidence=raw_evidence,
                completed_tools=completed_tools,
                pending_tools=pending_tools,
                failed_tools=failed_tools
            ):
                # Cancel all remaining tasks
                for task in pending_tasks:
                    task.cancel()
                log.info("Early stopping triggered. Cancelled remaining search tasks.")
                break
                
        duration = time.time() - start_time
        log.info(f"Research Orchestrator finished in {duration:.4f}s")
        
        return {
            "research_results": raw_evidence,
            "completed_tools": list(completed_tools),
            "failed_tools": list(failed_tools),
            "duration": duration
        }

    async def run_tool_safely(self, name: str, func, query: str, delay: float = 0.0):
        """
        Wrapper to run a tool safely. If it fails, the error is caught and logged,
        allowing other parallel tools to continue undisturbed.
        """
        if delay > 0:
            log.info(f"Staggering tool {name} by {delay}s to prevent rate limits.")
            await asyncio.sleep(delay)
            
        log.info(f"Tool started: {name}")
        
        # TASK 4: Automatic Search Fallback
        fallback_chain = []
        if name == "Web Search":
            fallback_chain = [("News Search", self.tool_map.get("News Search")), ("Wikipedia", self.tool_map.get("Wikipedia"))]
        elif name == "News Search":
            fallback_chain = [("Web Search", self.tool_map.get("Web Search")), ("Wikipedia", self.tool_map.get("Wikipedia"))]
            
        attempts = [(name, func)] + fallback_chain
        
        for tool_name, tool_func in attempts:
            if not tool_func: continue
            try:
                start_time = time.time()
                res = await tool_func(query)
                dur = time.time() - start_time
                if res and len(res) > 0:
                    log.info(f"Tool completed: {tool_name} - Duration: {dur:.2f}s - Found {len(res)} results.")
                    return (tool_name, "success", res)
                else:
                    log.warning(f"Tool {tool_name} returned 0 results. Trying next fallback.")
            except Exception as e:
                log.error(f"Tool failed: {tool_name} - Reason: {e}")
                
        return (name, "error", "All search tools in fallback chain failed or returned 0 results.")

class EvidenceCollector:
    """
    Normalizes, deduplicates, and validates the raw evidence collected by the Orchestrator.
    """
    def process(self, raw_evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        log.info(f"Evidence Collector processing {len(raw_evidence)} raw items.")
        
        seen_urls = set()
        normalized = []
        
        for item in raw_evidence:
            url = item.get("url", "")
            # Deduplicate by URL
            if url and url in seen_urls:
                continue
            if url:
                seen_urls.add(url)
                
            evidence = EvidenceItem(
                source=item.get("source", "Unknown"),
                title=item.get("title", "Untitled"),
                content=item.get("content", "No content available")[:2500], # Limit content length
                url=url,
                type="research_data"
            )
            normalized.append(evidence.model_dump())
            
        log.info(f"Evidence Collector yielded {len(normalized)} unique normalized items.")
        return normalized
