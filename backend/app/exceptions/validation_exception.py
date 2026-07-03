from app.exceptions.base_exception import BaseAppException

class ValidationException(BaseAppException):
    def __init__(self, agent_name: str, message: str):
        super().__init__(f"Validation failed in {agent_name}: {message}", type="ValidationException", retryable=True, agent=agent_name)
