import logging
from nexus_ai.core.llm import call_llm
logger = logging.getLogger(__name__)

class CoderAgent:
    SYSTEM = """You are a senior software architect and coder.
Given research findings or a technical task, produce:
- Architecture decisions with justification
- Code snippets, pseudocode, or system design
- Tech stack recommendations with reasoning
Be concrete and practical. Use markdown for code blocks.
Always include complete, runnable code blocks using markdown triple backticks.
Never summarize code — write the full implementation."""

    def code(self, research: str, task: str) -> str:
        logger.info(f"[Coder] generating technical output for: {task[:60]}")
        return call_llm(self.SYSTEM, f"Task: {task}\n\nResearch:\n{research}", max_tokens=600)