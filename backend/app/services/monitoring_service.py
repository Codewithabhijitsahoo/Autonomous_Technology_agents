import time
from typing import Dict, Any
from app.utils.logger import log

class MonitoringService:
    """
    A centralized Monitoring Service that tracks the health and performance 
    of the entire workflow, as specified in arch.md.
    """
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "workflow_duration": 0.0,
            "tool_failures": 0,
            "retry_attempts": 0,
            "llm_latency_total": 0.0,
            "search_latency_total": 0.0,
        }

    def log_node_start(self, node_name: str, stage: str, budget_remaining: float):
        log.info(f"[MONITOR] Stage: {stage} | Node: {node_name} | Budget Remaining: {budget_remaining:.2f}s")

    def log_llm_execution(self, model: str, latency: float, prompt_size: int, est_tokens: int):
        self.metrics["llm_latency_total"] += latency
        log.info(f"[MONITOR] LLM ({model}) - Latency: {latency:.2f}s | Prompt Size: {prompt_size} | Tokens: {est_tokens}")

    def log_tool_execution(self, tool_name: str, latency: float, success: bool):
        self.metrics["search_latency_total"] += latency
        if not success:
            self.metrics["tool_failures"] += 1
        status = "SUCCESS" if success else "FAILURE"
        log.info(f"[MONITOR] Tool ({tool_name}) - Latency: {latency:.2f}s | Status: {status}")

    def log_retry(self, component: str, attempt: int):
        self.metrics["retry_attempts"] += 1
        log.info(f"[MONITOR] Retry - {component} | Attempt: {attempt}")

    def get_metrics(self) -> Dict[str, Any]:
        return self.metrics

monitor = MonitoringService()
