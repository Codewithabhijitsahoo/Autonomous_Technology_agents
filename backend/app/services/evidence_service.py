import uuid
from datetime import datetime
from typing import List, Dict, Any
from app.schemas.evidence import EvidenceItem
from app.utils.logger import log

class EvidenceService:
    """
    Service responsible for strictly normalizing and organizing evidence.
    TASK 5: Deduplicates, merges, and removes empty/low-quality evidence.
    """
    def normalize(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        seen_urls = set()
        seen_content_hashes = set()
        
        for item in raw_items:
            # 1. Remove empty evidence
            content = item.get("content", "").strip()
            summary = item.get("summary", "").strip()
            if not content and not summary:
                log.warning("Skipping empty evidence item.")
                continue
                
            # 2. Deduplicate URLs
            url = item.get("url", "")
            if url and url in seen_urls:
                continue
            if url:
                seen_urls.add(url)
                
            # 3. Deduplicate exact content/facts (simple hash)
            content_hash = hash(content[:200]) # First 200 chars
            if content_hash in seen_content_hashes:
                continue
            seen_content_hashes.add(content_hash)
            
            try:
                # We map the raw output fields to our strict EvidenceItem schema
                evidence = EvidenceItem(
                    id=str(uuid.uuid4()),
                    source=item.get("source", "Unknown"),
                    tool=item.get("tool", item.get("source", "Unknown Tool")),
                    title=item.get("title", "Untitled"),
                    content=content,
                    summary=summary,
                    url=url,
                    authors=item.get("authors", []) if isinstance(item.get("authors"), list) else [item.get("authors")] if item.get("authors") else [],
                    published_date=item.get("published_date", item.get("published", "")),
                    retrieved_at=datetime.utcnow().isoformat(),
                    document_type=item.get("document_type", "research_data"),
                    metadata=item.get("metadata", {})
                )
                normalized.append(evidence.model_dump())
            except Exception as e:
                log.warning(f"Failed to normalize an evidence item. Skipping: {e}")
                continue
        return normalized

    def generate_statistics(self, normalized_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates collection statistics.
        """
        stats = {}
        total = len(normalized_evidence)
        for item in normalized_evidence:
            source = item.get("source", "Unknown")
            stats[source] = stats.get(source, 0) + 1
            
        stats_str = "\n".join([f"{k} Results: {v}" for k, v in stats.items()])
        stats_str += f"\nTotal Evidence: {total}"
        
        return {
            "counts_by_source": stats,
            "total": total,
            "summary_string": stats_str
        }
