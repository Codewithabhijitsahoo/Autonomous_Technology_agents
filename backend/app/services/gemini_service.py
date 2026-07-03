import time
from typing import Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from app.config.settings import settings
from app.utils.logger import log

class GeminiService:
    """
    A centralized, reusable service for interacting with Google Gemini models.
    Designed to be modular so future agents (Planner, Search, Validator) can use it directly.
    """
    def __init__(self):
        if not settings.google_api_key:
            log.warning("GOOGLE_API_KEY is not set. Gemini API calls will fail until configured.")
            
        def create_llm(model_name: str) -> ChatGoogleGenerativeAI:
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=settings.google_api_key,
                temperature=settings.gemini_temperature,
                max_tokens=settings.gemini_max_tokens,
                timeout=settings.gemini_timeout,
                max_retries=settings.gemini_max_retries,
            )

        # Dynamically fetch available models using the API key to route around limits/404s
        available_models = []
        try:
            import requests
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={settings.google_api_key}"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                for m in resp.json().get('models', []):
                    if 'generateContent' in m.get('supportedGenerationMethods', []):
                        name = m['name'].replace('models/', '')
                        available_models.append(name)
        except Exception as e:
            log.warning(f"Failed to fetch dynamic models: {e}")

        models_to_try = [settings.gemini_model]
        
        # Add dynamic models prioritizing flash then pro
        for m in available_models:
            if "flash" in m and "lite" not in m and "preview" not in m and m not in models_to_try:
                models_to_try.append(m)
        for m in available_models:
            if "pro" in m and "preview" not in m and m not in models_to_try:
                models_to_try.append(m)
                
        if len(models_to_try) == 1:
            default_fallbacks = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-flash-latest"]
            models_to_try.extend([m for m in default_fallbacks if m != settings.gemini_model])

        primary_llm = create_llm(models_to_try[0])
        if len(models_to_try) > 1:
            fallbacks = [create_llm(m) for m in models_to_try[1:10]]
            self.llm = primary_llm.with_fallbacks(fallbacks)
        else:
            self.llm = primary_llm

    async def chat(self, prompt: str) -> str:
        """
        Send a simple string prompt to Gemini and return the string response asynchronously.
        """
        start_time = time.time()
        log.info(f"Sending prompt request to Gemini (Model: {settings.gemini_model})")
        
        try:
            response = await self.llm.ainvoke(prompt)
            elapsed = time.time() - start_time
            log.info(f"Received response from Gemini in {elapsed:.2f}s")
            return response.content
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e) or repr(e)
            log.error(f"Gemini API request failed after {elapsed:.2f}s: {error_msg}")
            raise e

    async def structured_chat(self, prompt: str, schema: Any, system_prompt: str = "") -> Any:
        """
        Send a prompt with an optional system prompt and expect a structured JSON response matching the Pydantic schema.
        """
        start_time = time.time()
        log.info(f"Sending structured request to Gemini (Model: {settings.gemini_model})")
        
        try:
            structured_llm = self.llm.with_structured_output(schema)
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            response = await structured_llm.ainvoke(messages)
            
            elapsed = time.time() - start_time
            log.info(f"Received structured response from Gemini in {elapsed:.2f}s")
            return response
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e) or repr(e)
            log.error(f"Gemini structured API request failed after {elapsed:.2f}s: {error_msg}")
            raise e

    async def invoke(self, messages: List[BaseMessage], **kwargs: Any) -> Any:
        """
        Send structured LangChain messages to Gemini (useful for advanced agents).
        """
        start_time = time.time()
        log.info(f"Invoking Gemini with structured messages (Count: {len(messages)})")
        
        try:
            response = await self.llm.ainvoke(messages, **kwargs)
            elapsed = time.time() - start_time
            log.info(f"Received structured response from Gemini in {elapsed:.2f}s")
            return response
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e) or repr(e)
            log.error(f"Gemini structured invocation failed after {elapsed:.2f}s: {error_msg}")
            raise e
