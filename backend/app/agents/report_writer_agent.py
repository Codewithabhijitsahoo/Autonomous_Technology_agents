import time
import json
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.gemini_service import GeminiService
from app.prompts.report_prompt import REPORT_WRITER_PROMPT
from app.utils.logger import log
from app.services.prompt_builder_service import prompt_builder

class ReportWriterAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def write_report(self, query: str, knowledge: Dict[str, Any], insights: list, retries: int = 1) -> str:
        log.info("ReportWriterAgent started drafting report.")
        start_time = time.time()
        
        if not knowledge.get("topic_summaries") and not knowledge.get("facts") and not insights:
            log.warning("Knowledge and insights are completely empty. Generating fallback report.")
            return f"I could not find any reliable information for your query: **'{query}'**. This may be due to a lack of available data, search timeouts, or overly strict filtering thresholds. Please try rephrasing your search or using different keywords."
            
        # Phase 6: Use PromptBuilder for optimal context compression
        prompt = prompt_builder.build_report_prompt(knowledge, insights, query)
        
        # Determine if we need to chunk generation based on prompt size
        # Estimate using gemini_service if needed, but PromptBuilder guarantees it's fairly compressed.
        if len(prompt) > 30000:
            log.info("Payload is very large. Generating report section-by-section.")
            sections = ["Executive Summary", "Technology Highlights", "Competitor Analysis", "Market Trends", "Risks", "Opportunities", "Recommendations", "References"]
            
            final_report = []
            
            for section in sections:
                section_prompt = f"Write the '{section}' section based on this context:\n\n{prompt}"
                messages = [
                    SystemMessage(content=REPORT_WRITER_PROMPT),
                    HumanMessage(content=section_prompt)
                ]
                try:
                    response = await self.gemini_service.invoke(messages)
                    final_report.append(f"## {section}\n\n" + response.content)
                except Exception as e:
                    log.warning(f"Failed to generate section {section}: {e}")
                    
            duration = time.time() - start_time
            log.info(f"Section-by-section ReportWriterAgent completed in {duration:.4f}s.")
            return "\n\n".join(final_report)
            
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
