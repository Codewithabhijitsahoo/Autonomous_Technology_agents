from app.exceptions.base_exception import BaseAppException

class ToolException(BaseAppException):
    def __init__(self, tool_name: str, message: str, retryable: bool = True):
        super().__init__(f"Tool {tool_name} failed: {message}", type="ToolException", retryable=retryable)
