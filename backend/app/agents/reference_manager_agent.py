import time
import uuid
from typing import List, Dict, Any
from pydantic import BaseModel
from app.utils.logger import log

class ReferenceManagerAgent:
    """
    Service responsible for collecting every source, generating a unique source ID,
    and maintaining a reference map throughout the workflow.
    """
    async def process_references(self, raw_evidence: List[Dict[str, Any]]) -> dict:
        log.info("ReferenceManagerAgent starting.")
        start_time = time.time()
        
        reference_map = {}
        traceable_evidence = []
        
        for idx, item in enumerate(raw_evidence):
            source_id = f"SRC-{uuid.uuid4().hex[:8].upper()}"
            evidence_id = f"EVID-{uuid.uuid4().hex[:8].upper()}"
            citation_id = f"[{idx + 1}]"
            
            ref_data = {
                "source_id": source_id,
                "citation_id": citation_id,
                "url": item.get("url", ""),
                "title": item.get("title", "Untitled Source"),
                "domain": item.get("url", "").split("/")[2] if "://" in item.get("url", "") else "Unknown",
                "source_type": item.get("type", "research_data"),
                "tool_used": item.get("source", "Unknown Tool"),
                "timestamp": time.time()
            }
            
            reference_map[source_id] = ref_data
            
            # Enrich evidence with traceability
            enriched_item = item.copy()
            enriched_item["evidence_id"] = evidence_id
            enriched_item["source_id"] = source_id
            enriched_item["citation_id"] = citation_id
            traceable_evidence.append(enriched_item)
            
        log.info(f"ReferenceManagerAgent mapped {len(reference_map)} sources in {time.time() - start_time:.2f}s")
        
        return {
            "reference_map": reference_map,
            "traceable_evidence": traceable_evidence,
            "citations": [v for k, v in reference_map.items()]
        }
