import logging
from nexus_ai.core.llm import call_llm
logger = logging.getLogger(__name__)

class CriticAgent:
    SYSTEM = """You are a harsh but fair critic reviewing an AI-generated response.
Identify:
- Logical flaws or gaps
- Missing considerations
- Weak or vague recommendations
- Factual concerns
Be specific. Output a numbered list of issues found, then a score out of 10."""

    def critique(self, content: str) -> str:
        logger.info("[Critic] reviewing output")
        return call_llm(self.SYSTEM, f"Critique this output:\n\n{content}", max_tokens=400)