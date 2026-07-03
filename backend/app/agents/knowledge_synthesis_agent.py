import time
import json
import asyncio
from typing import List, Dict, Any
from app.services.gemini_service import GeminiService
from app.services.knowledge_service import KnowledgeService
from app.prompts.knowledge_prompt import KNOWLEDGE_SYNTHESIS_PROMPT
from app.schemas.knowledge import StructuredKnowledge
from app.utils.logger import log

class KnowledgeSynthesisAgent:
    """Agent responsible for transforming validated evidence into structured knowledge and graphs."""
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.knowledge_service = KnowledgeService()

    async def synthesize(self, validated_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        log.info(f"KnowledgeSynthesisAgent started processing {len(validated_evidence)} valid items.")
        start_time = time.time()
        
        if not validated_evidence:
            log.warning("No validated evidence available for synthesis.")
            return StructuredKnowledge().model_dump()

        # Execute chunks concurrently
        chunks = self.knowledge_service.chunk_evidence(validated_evidence)
        tasks = []
        for i, chunk in enumerate(chunks):
            tasks.append(self._process_chunk(chunk, i))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results = []
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                log.error(f"Chunk {i} failed: {res}")
            else:
                valid_results.append(res)
                
        log.info(f"KnowledgeSynthesisAgent successfully processed {len(valid_results)}/{len(chunks)} chunks.")
        
        # Merge all partial knowledge structures
        final_knowledge = self.knowledge_service.merge_knowledge(valid_results)
        
        duration = time.time() - start_time
        log.info(f"Knowledge synthesis completed in {duration:.4f}s.")
        log.info(f"Extracted {len(final_knowledge.entities)} entities, {len(final_knowledge.facts)} facts, {len(final_knowledge.knowledge_graph.nodes)} graph nodes.")
        
        return final_knowledge.model_dump()

    async def _process_chunk(self, chunk: List[Dict[str, Any]], chunk_index: int, retries: int = 0) -> StructuredKnowledge:
        chunk_json = json.dumps(chunk, indent=2)
        prompt = f"Synthesize the following validated evidence into structured knowledge:\n\n{chunk_json}"
        
        for attempt in range(retries + 1):
            try:
                log.info(f"Processing chunk {chunk_index} (Attempt {attempt+1}/{retries+1})")
                result: StructuredKnowledge = await self.gemini_service.structured_chat(
                    prompt=prompt,
                    schema=StructuredKnowledge,
                    system_prompt=KNOWLEDGE_SYNTHESIS_PROMPT
                )
                return result
            except Exception as e:
                log.warning(f"Chunk {chunk_index} attempt {attempt+1} failed: {e}")
                if attempt == retries:
                    raise e
