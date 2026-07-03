import json
from typing import List, Dict, Any
from app.schemas.knowledge import StructuredKnowledge
from app.utils.logger import log

class KnowledgeService:
    """Service to handle chunking, merging, and formatting of knowledge synthesis."""

    def chunk_evidence(self, validated_evidence: List[Dict[str, Any]], max_chars: int = 20000) -> List[List[Dict[str, Any]]]:
        """
        Splits evidence into chunks to prevent exceeding model context limits.
        Automatically chunks by character length of the serialized item.
        """
        chunks = []
        current_chunk = []
        current_length = 0
        
        for item in validated_evidence:
            item_str = json.dumps(item)
            item_len = len(item_str)
            
            if current_length + item_len > max_chars and current_chunk:
                chunks.append(current_chunk)
                current_chunk = [item]
                current_length = item_len
            else:
                current_chunk.append(item)
                current_length += item_len
                
        if current_chunk:
            chunks.append(current_chunk)
            
        log.info(f"Chunked {len(validated_evidence)} evidence items into {len(chunks)} chunks.")
        return chunks

    def merge_knowledge(self, knowledge_list: List[StructuredKnowledge]) -> StructuredKnowledge:
        """
        Merges partial structured knowledge artifacts from multiple chunks.
        """
        if not knowledge_list:
            return StructuredKnowledge()
            
        if len(knowledge_list) == 1:
            return knowledge_list[0]
            
        merged = StructuredKnowledge()
        exec_summaries = []
        seen_nodes = set()
        seen_edges = set()
        
        for k in knowledge_list:
            if k.executive_summary:
                exec_summaries.append(k.executive_summary)
            merged.topic_summaries.extend(k.topic_summaries)
            merged.entities.extend(k.entities)
            merged.facts.extend(k.facts)
            merged.timelines.extend(k.timelines)
            merged.relationships.extend(k.relationships)
            merged.statistics.extend(k.statistics)
            merged.terminology.extend(k.terminology)
            
            for node in k.knowledge_graph.nodes:
                if node.id not in seen_nodes:
                    merged.knowledge_graph.nodes.append(node)
                    seen_nodes.add(node.id)
                    
            for edge in k.knowledge_graph.edges:
                edge_id = f"{edge.source}-{edge.target}-{edge.relationship}"
                if edge_id not in seen_edges:
                    merged.knowledge_graph.edges.append(edge)
                    seen_edges.add(edge_id)
                    
        # Combine executive summaries into a mega-draft
        merged.executive_summary = "\n\n".join(exec_summaries)
        return merged
