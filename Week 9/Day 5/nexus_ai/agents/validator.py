import logging
from nexus_ai.core.llm import call_llm
from nexus_ai.config import MIN_VALID_LEN
logger = logging.getLogger(__name__)

class ValidatorAgent:
    SYSTEM = """You are a quality validator for AI outputs.
Check the response for: completeness, clarity, relevance to the task, and actionability.
If it passes: start with "PASS " then a one-line quality note.
If it fails: start with "FAIL " then specific reasons.
Then always append the original content."""

    def validate(self, content: str, task: str) -> tuple[bool, str]:
        logger.info("[Validator] validating final output")
        if len(content.strip()) < MIN_VALID_LEN:
            return False, f"FAIL  Response too short ({len(content)} chars).\n\n{content}"
        result = call_llm(self.SYSTEM, f"Task: {task}\n\nOutput to validate:\n{content}", max_tokens=600)
        passed = result.strip().startswith("PASS")
        return passed, result