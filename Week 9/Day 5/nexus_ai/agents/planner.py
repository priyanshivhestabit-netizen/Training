import json, logging
from nexus_ai.core.llm import call_llm
logger = logging.getLogger(__name__)

class PlannerAgent:
    SYSTEM = """You are a strategic task planner for an autonomous AI system.
Break the user task into 4-6 clear, specific, sequential subtasks.
Each subtask must be actionable by a specialist agent (Researcher, Coder, Analyst, etc.).
Return ONLY a valid JSON array of strings. No markdown, no explanation.
Example: ["subtask 1", "subtask 2", "subtask 3"]"""

    def plan(self, task: str) -> list[str]:
        logger.info(f"[Planner] planning: {task[:60]}")
        raw = call_llm(self.SYSTEM, f"Create a plan for: {task}", max_tokens=400)
        try:
            s, e = raw.find("["), raw.rfind("]") + 1
            return json.loads(raw[s:e])
        except Exception:
            logger.warning("[Planner] JSON parse failed, using fallback plan")
            return [
                f"Research background and context of: {task}",
                f"Identify key components and requirements for: {task}",
                f"Design a technical approach for: {task}",
                f"Analyze risks and opportunities in: {task}",
                f"Generate actionable recommendations for: {task}",
            ]