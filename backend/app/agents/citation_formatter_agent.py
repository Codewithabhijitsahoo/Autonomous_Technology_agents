import time
from typing import List, Dict, Any
from app.services.gemini_service import GeminiService
from app.utils.logger import log

class CitationFormatterAgent:
    """
    Appends the References section to the final report and formats the final JSON payload.
    """
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def format_citations(self, reviewed_report: str, reference_map: Dict[str, Any]) -> dict:
        log.info("CitationFormatterAgent starting.")
        start_time = time.time()
        
        # Build Markdown References Section
        references_section = "\n\n## References\n"
        citations_list = []
        
        for src_id, ref in reference_map.items():
            citations_list.append({
                "id": ref["citation_id"],
                "title": ref["title"],
                "url": ref["url"],
                "domain": ref["domain"]
            })
            references_section += f"{ref['citation_id']} {ref['title']}\n{ref['url']}\n\n"
            
        final_markdown = reviewed_report + references_section
        
        log.info(f"CitationFormatterAgent finished in {time.time() - start_time:.2f}s")
        
        return {
            "formatted_report": final_markdown,
            "citations": citations_list
        }
