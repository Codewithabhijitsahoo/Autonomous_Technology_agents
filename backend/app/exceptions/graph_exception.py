from app.exceptions.base_exception import BaseAppException

class GraphException(BaseAppException):
    def __init__(self, node_name: str, message: str):
        super().__init__(f"Node {node_name} failed: {message}", type="GraphException", retryable=False, node=node_name)
