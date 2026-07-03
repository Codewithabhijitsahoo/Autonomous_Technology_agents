import asyncio
from typing import Callable, Any
from app.utils.logger import log

class RetryService:
    @staticmethod
    async def retry_async(func: Callable, retries: int = 2, base_delay: float = 1.0, exceptions_to_catch: tuple = (Exception,)) -> Any:
        for attempt in range(retries + 1):
            try:
                return await func()
            except exceptions_to_catch as e:
                if hasattr(e, "retryable") and not e.retryable:
                    log.error(f"Non-retryable exception caught: {e}")
                    raise e
                    
                if attempt == retries:
                    log.error(f"Function {func.__name__} failed after {retries} retries: {e}")
                    raise e
                    
                delay = base_delay * (2 ** attempt)
                log.warning(f"Attempt {attempt+1} failed. Retrying in {delay}s... Error: {e}")
                await asyncio.sleep(delay)
