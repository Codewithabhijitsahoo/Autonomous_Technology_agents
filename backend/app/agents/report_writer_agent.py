import time
import json
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.gemini_service import GeminiService
from app.prompts.report_prompt import REPORT_WRITER_PROMPT
from app.utils.logger import log

class ReportWriterAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def write_report(self, query: str, knowledge: Dict[str, Any], insights: list, retries: int = 1) -> str:
        log.info("ReportWriterAgent started drafting report.")
        start_time = time.time()
        
        # Prevent hallucinated reports on empty data
        if not knowledge.get("topic_summaries") and not knowledge.get("facts") and not insights:
            log.warning("Knowledge and insights are completely empty. Generating fallback report.")
            return f"I could not find any reliable information for your query: **'{query}'**. This may be due to a lack of available data, search timeouts, or overly strict filtering thresholds. Please try rephrasing your search or using different keywords."
            
        payload = {
            "knowledge": knowledge,
            "insights": insights
        }
        
        # Keep payload manageable
        payload_json = json.dumps(payload, indent=2)
        if len(payload_json) > 80000:
            payload_json = payload_json[:80000] + "\n...[TRUNCATED]"
            
        prompt = f"Write a comprehensive research report using the following validated data and insights:\n\n{payload_json}"
        messages = [
            SystemMessage(content=REPORT_WRITER_PROMPT),
            HumanMessage(content=prompt)
        ]
        
        for attempt in range(retries + 1):
            try:
                log.info(f"Writing report (Attempt {attempt+1}/{retries+1})")
                response = await self.gemini_service.invoke(messages)
                
                duration = time.time() - start_time
                log.info(f"ReportWriterAgent completed in {duration:.4f}s.")
                return response.content
                
            except Exception as e:
                log.warning(f"Report generation attempt {attempt+1} failed: {e}")
                if attempt == retries:
                    log.error(f"ReportWriterAgent failed completely: {e}")
                    return f"# Error Generating Report\n\nThe system encountered an error while drafting the report for your query: **'{query}'**.\n\nPlease try again later."
