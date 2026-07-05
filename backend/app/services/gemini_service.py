import time
from typing import Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from app.config.settings import settings
from app.utils.logger import log
from app.services.monitoring_service import monitor

class GeminiService:
    """
    A centralized, reusable service for interacting with Google Gemini models.
    Implements Intelligent Multi-Model Orchestration and Fault Tolerance.
    """
    def __init__(self):
        if not settings.google_api_key:
            log.warning("GOOGLE_API_KEY is not set. Gemini API calls will fail until configured.")
            
        self.default_model = settings.gemini_model
        
    def _create_llm(self, model_name: str) -> ChatGoogleGenerativeAI:
        # Implements Automatic retry for transient failures (429, 503, timeout)
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=settings.google_api_key,
            temperature=settings.gemini_temperature,
            max_tokens=settings.gemini_max_tokens,
            max_retries=settings.gemini_max_retries,
        )

    def route_model(self, task_type: str, complexity: str = "Simple") -> ChatGoogleGenerativeAI:
        """
        Intelligent Multi-Model Orchestration (Model Router)
        """
        # TASK 9: Optimize Model Routing
        if task_type in ["query_understanding", "intent_detection", "planning", "search_strategy", "validation"]:
            primary = "gemini-2.5-flash"
        elif task_type in ["knowledge_synthesis", "insight_generation", "deep_reasoning"] or ("Complex" in complexity and task_type != "report_generation"):
            primary = "gemini-2.5-pro"
        elif task_type == "report_generation" or "Very Complex" in complexity:
            primary = "gemini-3.1-pro" # Note: using 3.1 as it is the current version
        else:
            primary = self.default_model

        # Model Failover (Graceful degradation)
        if "pro" in primary:
            fallbacks = [
                self._create_llm("gemini-2.5-pro"),
                self._create_llm("gemini-1.5-pro"),
                self._create_llm("gemini-2.5-flash") # Ultimate fallback
            ]
        else:
            fallbacks = [
                self._create_llm("gemini-2.0-flash"),
                self._create_llm("gemini-1.5-flash")
            ]
        
        primary_llm = self._create_llm(primary)
        return primary_llm.with_fallbacks(fallbacks)

    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4
        

        
    def _compress_prompt(self, prompt: str, token_limit: int) -> str:
        # TASK 8: Prompt Budget System
        est_tokens = self.estimate_tokens(prompt)
        if est_tokens <= token_limit:
            return prompt
            
        log.warning(f"Prompt size {est_tokens} exceeds budget {token_limit}. Compressing...")
        
        # 1. Remove repeated metadata/instructions by splitting and deduplicating lines
        lines = prompt.split('\n')
        seen = set()
        compressed = []
        for line in lines:
            line_strip = line.strip()
            # keep short lines like headers, but deduplicate long repetitive lines
            if len(line_strip) < 30 or line_strip not in seen:
                compressed.append(line)
                if len(line_strip) >= 30:
                    seen.add(line_strip)
                    
        result = '\n'.join(compressed)
        
        # 2. Hard truncate if still too large
        char_limit = token_limit * 4
        if len(result) > char_limit:
            log.warning("Prompt still exceeds limit after deduplication. Hard truncating.")
            result = result[:char_limit] + "\n...[Content Truncated due to Prompt Budget]..."
            
        return result

    async def chat(self, prompt: str, task_type: str = "general", complexity: str = "Simple") -> str:
        """
        Send a simple string prompt to Gemini and return the string response asynchronously.
        Enforces a Prompt Budget.
        """
        start_time = time.time()
        
        char_count = len(prompt)
        est_tokens = self.estimate_tokens(prompt)
        token_limit = 30000
        
        llm = self.route_model(task_type, complexity)
        model_name = getattr(llm, 'model', settings.gemini_model)
        
        log.info(f"Prompt Size Check - Characters: {char_count}, Estimated Tokens: {est_tokens}, Limit: {token_limit}")
        
        if est_tokens > token_limit:
            log.warning(f"Prompt exceeds limit ({est_tokens} > {token_limit}). Splitting automatically.")
            char_limit = token_limit * 4
            chunks = [prompt[i:i + char_limit] for i in range(0, len(prompt), char_limit)]
            log.info(f"Chunk Count: {len(chunks)}")
            
            results = []
            for i, chunk in enumerate(chunks):
                log.info(f"Processing chunk {i+1}/{len(chunks)}...")
                try:
                    c_start = time.time()
                    response = await llm.ainvoke(chunk)
                    results.append(response.content)
                    monitor.log_llm_execution(model_name, time.time() - c_start, len(chunk), self.estimate_tokens(chunk))
                except Exception as e:
                    log.error(f"Chunk {i+1} failed: {e}")
                    monitor.log_retry("Gemini Chat Chunk", 1)
                    results.append(f"[Chunk {i+1} Failed: {e}]")
            
            elapsed = time.time() - start_time
            log.info(f"Completed {len(chunks)} chunks in {elapsed:.2f}s")
            return "\n\n".join(results)

        log.info(f"Sending prompt request to Gemini (Model: {model_name})")
        
        prompt = self._compress_prompt(prompt, 15000) # Enforce 15000 token budget
        est_tokens = self.estimate_tokens(prompt)
        
        try:
            response = await llm.ainvoke(prompt)
            elapsed = time.time() - start_time
            log.info(f"Received response from Gemini in {elapsed:.2f}s")
            monitor.log_llm_execution(model_name, elapsed, char_count, est_tokens)
            return response.content
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e) or repr(e)
            log.error(f"Gemini API request failed after {elapsed:.2f}s: {error_msg}")
            raise e

    async def structured_chat(self, prompt: str, schema: Any, system_prompt: str = "", task_type: str = "general", complexity: str = "Simple") -> Any:
        """
        Send a prompt with an optional system prompt and expect a structured JSON response matching the Pydantic schema.
        """
        start_time = time.time()
        llm = self.route_model(task_type, complexity)
        model_name = getattr(llm, 'model', settings.gemini_model)
        log.info(f"Sending structured request to Gemini (Model: {model_name})")
        
        try:
            structured_llm = llm.with_structured_output(schema)
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
                
            compressed_prompt = self._compress_prompt(prompt, 15000)
            messages.append(HumanMessage(content=compressed_prompt))
            
            
            response = await structured_llm.ainvoke(messages)
            
            elapsed = time.time() - start_time
            log.info(f"Received structured response from Gemini in {elapsed:.2f}s")
            monitor.log_llm_execution(model_name, elapsed, len(prompt), self.estimate_tokens(prompt))
            return response
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e) or repr(e)
            log.error(f"Gemini structured API request failed after {elapsed:.2f}s: {error_msg}")
            raise e

    async def invoke(self, messages: List[BaseMessage], task_type: str = "general", complexity: str = "Simple", **kwargs: Any) -> Any:
        """
        Send structured LangChain messages to Gemini (useful for advanced agents).
        """
        start_time = time.time()
        llm = self.route_model(task_type, complexity)
        model_name = getattr(llm, 'model', settings.gemini_model)
        log.info(f"Invoking Gemini with structured messages (Count: {len(messages)}, Model: {model_name})")
        
        try:
            response = await llm.ainvoke(messages, **kwargs)
            elapsed = time.time() - start_time
            log.info(f"Received structured response from Gemini in {elapsed:.2f}s")
            
            total_content = sum([len(m.content) for m in messages if isinstance(m.content, str)])
            monitor.log_llm_execution(model_name, elapsed, total_content, self.estimate_tokens(" ".join([m.content for m in messages if isinstance(m.content, str)])))
            return response
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e) or repr(e)
            log.error(f"Gemini structured invocation failed after {elapsed:.2f}s: {error_msg}")
            raise e
