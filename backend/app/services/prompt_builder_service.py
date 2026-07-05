import json
from typing import Dict, Any, List
from app.utils.logger import log

class PromptBuilderService:
    """
    Adaptive Prompt Builder Service.
    Responsible for estimating tokens, removing duplicated context,
    compressing evidence, and building the smallest prompt possible.
    """
    def __init__(self):
        # rough estimation, 1 token ~ 4 characters
        self.char_per_token = 4
        self.max_tokens = 6000 # aggressive context compression threshold

    def estimate_tokens(self, text: str) -> int:
        return len(text) // self.char_per_token

    def _compress_json(self, data: Any) -> str:
        """Helper to safely format json tightly."""
        if isinstance(data, (dict, list)):
            return json.dumps(data, separators=(',', ':'))
        return str(data)

    def build_synthesis_prompt(self, evidence: List[Dict[str, Any]], query: str, references: Dict[str, Any]) -> str:
        """Task 3: Synthesis should only receive verified evidence, references, and query."""
        compressed_evidence = []
        # deduplicate during compression
        seen_content = set()
        for item in evidence:
            content = item.get("content", "")
            if not content: continue
            content_hash = hash(content[:200])
            if content_hash not in seen_content:
                compressed_evidence.append({
                    "title": item.get("title", ""),
                    "content": content[:1500], # limit length
                    "source": item.get("source", "")
                })
                seen_content.add(content_hash)
                
        prompt = f"Query: {query}\nEvidence:\n{self._compress_json(compressed_evidence)}\nReferences:\n{self._compress_json(references)}"
        
        tokens = self.estimate_tokens(prompt)
        if tokens > self.max_tokens:
            log.warning(f"Synthesis prompt too large ({tokens} tokens). Truncating evidence.")
            # aggressive truncation if still too large
            truncated_evidence = compressed_evidence[:len(compressed_evidence)//2]
            prompt = f"Query: {query}\nEvidence:\n{self._compress_json(truncated_evidence)}\nReferences:\n{self._compress_json(references)}"
            
        return prompt

    def build_insight_prompt(self, knowledge: Dict[str, Any], query: str) -> str:
        """Task 4: Insight receives summary, facts, entities, query only."""
        summary = knowledge.get("executive_summary", "")
        facts = knowledge.get("timeline_events", [])[:5] # top facts
        entities = knowledge.get("key_entities", [])[:10]
        
        payload = {
            "summary": summary,
            "top_facts": facts,
            "key_entities": entities
        }
        return f"Query: {query}\nKnowledge Base:\n{self._compress_json(payload)}"
        
    def build_report_prompt(self, knowledge: Dict[str, Any], insights: Dict[str, Any], query: str) -> str:
        """Task 5: Report receives summary, insights, query only."""
        payload = {
            "summary": knowledge.get("executive_summary", ""),
            "topic_summaries": knowledge.get("topic_summaries", {}),
            "insights": insights
        }
        return f"Query: {query}\nContext:\n{self._compress_json(payload)}"

prompt_builder = PromptBuilderService()
