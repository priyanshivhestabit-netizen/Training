import logging
from nexus_ai.core.llm import call_llm
logger = logging.getLogger(__name__)

class AnalystAgent:
    SYSTEM = """You are a business and technical analyst.
Given a set of research and implementation outputs, produce:
- SWOT or risk/opportunity analysis
- Key metrics to track
- Prioritized recommendations
- Feasibility assessment
Be data-driven and structured."""

    def analyze(self, combined_outputs: str, task: str) -> str:
        logger.info(f"[Analyst] analyzing outputs for: {task[:60]}")
        return call_llm(self.SYSTEM, f"Task: {task}\n\nOutputs to analyze:\n{combined_outputs}", max_tokens=500)