class BaseAppException(Exception):
    def __init__(self, message: str, type: str = "BaseException", retryable: bool = False, agent: str = None, node: str = None):
        self.message = message
        self.type = type
        self.retryable = retryable
        self.agent = agent
        self.node = node
        super().__init__(self.message)
