import logging
from autogen import AssistantAgent
from config import LLM_CONFIG

logger = logging.getLogger(__name__)


class WorkerAgent:
    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.name = f"Worker-{worker_id}"

        self.agent = AssistantAgent(
            name=f"worker_{worker_id}",
            system_message="""
You are a focused research worker. You will be given one specific task.

Execute only that task.
Be factual, concise, and structured.
Do not go beyond the scope of the task given.
""",
            llm_config=LLM_CONFIG
        )

    def execute(self, task):
        try:
            logger.info(f"{self.name} started task: {task}")

            reply = self.agent.generate_reply(
                messages=[
                    {
                        "role": "user",
                        "content": task
                    }
                ]
            )

            logger.info(f"{self.name} finished task")

            return f"[{self.name}]\n{str(reply)}"

        except Exception as e:
            logger.error(f"{self.name} error: {e}")
            return f"{self.name} failed."