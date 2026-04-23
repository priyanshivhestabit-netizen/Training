import logging
from nexus_ai.core.llm import call_llm
logger = logging.getLogger(__name__)

class ResearcherAgent:
    SYSTEM = """You are a research specialist. Given a specific subtask, gather relevant
facts, frameworks, and context STRICTLY related to the current task.
Do NOT bring in context from unrelated previous tasks.
Be concise and focused. Bullet points only."""

    def research(self, subtask: str, memory_context: str = "") -> str:
        logger.info(f"[Researcher] researching: {subtask[:60]}")
        user = f"Memory context:\n{memory_context}\n\nResearch this: {subtask}" if memory_context else f"Research this: {subtask}"
        return call_llm(self.SYSTEM, user, max_tokens=500)