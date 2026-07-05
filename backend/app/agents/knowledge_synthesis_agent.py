import time
import json
import asyncio
from typing import List, Dict, Any
from app.services.gemini_service import GeminiService
from app.services.knowledge_service import KnowledgeService
from app.prompts.knowledge_prompt import KNOWLEDGE_SYNTHESIS_PROMPT
from app.schemas.knowledge import StructuredKnowledge
from app.utils.logger import log
from app.services.prompt_builder_service import prompt_builder

class KnowledgeSynthesisAgent:
    """Agent responsible for transforming validated evidence into structured knowledge and graphs."""
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.knowledge_service = KnowledgeService()

    async def synthesize(self, validated_evidence: List[Dict[str, Any]], query: str = "", references: Dict[str, Any] = None) -> Dict[str, Any]:
        log.info(f"KnowledgeSynthesisAgent started processing {len(validated_evidence)} valid items.")
        start_time = time.time()
        
        if not validated_evidence:
            log.warning("No validated evidence available for synthesis.")
            return StructuredKnowledge().model_dump()

        if references is None: references = {}

        # Use PromptBuilderService to heavily compress and format the prompt
        prompt = prompt_builder.build_synthesis_prompt(validated_evidence, query, references)

        valid_results = []
        # Since PromptBuilder truncates to a strict threshold, we can mostly skip chunking 
        # unless it is absurdly large. We will treat the result of prompt_builder as 1 chunk.
        log.info("Sending compressed evidence to synthesis.")
        try:
            result = await self._process_chunk(prompt, 0)
            valid_results.append(result)
        except Exception as e:
            log.error(f"Single chunk processing failed: {e}")
        # Removing multi-chunking loop since PromptBuilder handles length constraints
        
        # Merge all partial knowledge structures
        final_knowledge = self.knowledge_service.merge_knowledge(valid_results)
        
        duration = time.time() - start_time
        log.info(f"Knowledge synthesis completed in {duration:.4f}s.")
        log.info(f"Extracted {len(final_knowledge.entities)} entities, {len(final_knowledge.facts)} facts, {len(final_knowledge.knowledge_graph.nodes)} graph nodes.")
        
        return final_knowledge.model_dump()

    async def hierarchical_synthesize(self, subtask_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        log.info(f"Hierarchical Synthesis starting for {len(subtask_evidence)} subtasks.")
        start_time = time.time()
        
        tasks = []
        for i, subtask in enumerate(subtask_evidence):
            task_name = subtask.get("task", f"Subtask {i}")
            evidence = subtask.get("evidence", [])
            tasks.append(self._process_subtask_summary(task_name, evidence, i))
            
        local_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_local_results = []
        for res in local_results:
            if not isinstance(res, Exception):
                valid_local_results.append(res)
                
        final_knowledge = self.knowledge_service.merge_knowledge(valid_local_results)
        
        duration = time.time() - start_time
        log.info(f"Hierarchical Synthesis completed in {duration:.4f}s.")
        return final_knowledge.model_dump()

    async def _process_subtask_summary(self, task_name: str, evidence: List[Dict[str, Any]], index: int) -> StructuredKnowledge:
        log.info(f"Generating Local Summary for subtask: {task_name}")
        chunk_json = json.dumps(evidence, indent=2)
        prompt = f"Synthesize the following evidence specifically for the research objective: '{task_name}' into structured knowledge:\n\n{chunk_json}"
        
        try:
            result: StructuredKnowledge = await self.gemini_service.structured_chat(
                prompt=prompt,
                schema=StructuredKnowledge,
                system_prompt=KNOWLEDGE_SYNTHESIS_PROMPT
            )
            return result
        except Exception as e:
            log.error(f"Local Summary for {task_name} failed: {e}")
            raise e

    async def _process_chunk(self, prompt: str, chunk_index: int, retries: int = 0) -> StructuredKnowledge:
        
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
