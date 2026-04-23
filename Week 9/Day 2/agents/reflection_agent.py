import logging
from autogen import AssistantAgent
from config import LLM_CONFIG

logger = logging.getLogger(__name__)


class ReflectionAgent:
    def __init__(self):
        self.name = "Reflection Agent"

        self.agent = AssistantAgent(
            name="reflection_agent",
            system_message="""
You are an editor and critic. You will receive multiple outputs from different workers.

Your job is to:
- Merge and deduplicate overlapping content
- Improve clarity and structure
- Remove redundancy
- Produce one clean, unified, well-organized draft

Do not add new facts. Only improve what is given.
""",
            llm_config=LLM_CONFIG
        )

    def improve(self, worker_outputs):
        try:
            logger.info("ReflectionAgent improving outputs")

            combined = "\n\n".join(worker_outputs)

            reply = self.agent.generate_reply(
                messages=[
                    {
                        "role": "user",
                        "content": f"Improve and unify these worker outputs:\n\n{combined}"
                    }
                ]
            )

            return str(reply)

        except Exception as e:
            logger.error(f"Reflection error: {e}")
            return "Reflection failed."