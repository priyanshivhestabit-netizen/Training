import logging
from nexus_ai.core.llm import call_llm
logger = logging.getLogger(__name__)

class OptimizerAgent:
    SYSTEM = """You are an expert editor and optimizer.
You receive a draft output and a critique. Your job is to:
- Fix the issues raised by the critic
- Strengthen weak points
- Remove redundancy
- Improve clarity and structure
Return the improved version only. No meta-commentary."""

    def optimize(self, draft: str, critique: str) -> str:
        logger.info("[Optimizer] improving draft based on critique")
        return call_llm(
            self.SYSTEM,
            f"Draft:\n{draft}\n\nCritique:\n{critique}\n\nProduce the improved version:",
            max_tokens=700
        )