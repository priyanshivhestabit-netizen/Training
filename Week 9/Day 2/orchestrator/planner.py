import logging
import json
from autogen import AssistantAgent
from config import LLM_CONFIG

logger = logging.getLogger(__name__)


class Planner:
    def __init__(self):
        self.name = "Planner Agent"

        self.agent = AssistantAgent(
            name="planner_agent",
            system_message="""
You are a task planner.

Given a user query, break it down into exactly 3 specific,
actionable research subtasks for worker agents.

Respond ONLY with a valid JSON array of 3 strings.

No explanation.
No markdown.
No extra text.

Example:
["subtask one", "subtask two", "subtask three"]
""",
            llm_config=LLM_CONFIG
        )

    def create_plan(self, query: str):
        try:
            logger.info("Planner creating plan")

            reply = self.agent.generate_reply(
                messages=[
                    {
                        "role": "user",
                        "content": f"Break this query into 3 subtasks: {query}"
                    }
                ]
            )

            raw = str(reply).strip()

            # Safely extract JSON array
            start = raw.find("[")
            end = raw.rfind("]") + 1

            steps = json.loads(raw[start:end])

            return steps

        except Exception as e:
            logger.error(f"Planner error: {e}")

            # Fallback plan
            return [
                f"Research core concepts of: {query}",
                f"Find practical examples of: {query}",
                f"List benefits and challenges of: {query}"
            ]