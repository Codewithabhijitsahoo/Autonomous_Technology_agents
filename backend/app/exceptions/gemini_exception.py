from app.exceptions.base_exception import BaseAppException

class GeminiException(BaseAppException):
    def __init__(self, message: str, retryable: bool = False, agent: str = None, node: str = None):
        super().__init__(message, type="GeminiException", retryable=retryable, agent=agent, node=node)

class GeminiQuotaExceeded(GeminiException):
    def __init__(self, agent: str = None, node: str = None):
        super().__init__("You have reached the Gemini API quota. Please try again later.", retryable=False, agent=agent, node=node)

class GeminiInvalidKey(GeminiException):
    def __init__(self, agent: str = None, node: str = None):
        super().__init__("Invalid Gemini API Key.", retryable=False, agent=agent, node=node)

class GeminiTimeout(GeminiException):
    def __init__(self, agent: str = None, node: str = None):
        super().__init__("Gemini API request timed out.", retryable=True, agent=agent, node=node)
