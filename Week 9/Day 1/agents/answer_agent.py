from config import LLM_CONFIG
from autogen import AssistantAgent

class AnswerAgent:
    def __init__(self):
        self.name = "Answer Agent"

        self.agent = AssistantAgent(
            name="answer_agent",
            system_message="""
You provide the final polished answer to the user.
Use the summary provided to craft a clear, well-written, and helpful response.
Write in a natural, conversational tone directed at the user.
Do not mention that you received a summary.
""",
            llm_config=LLM_CONFIG
        )

    def process(self, summary_text: str) -> str:
        reply = self.agent.generate_reply(
            messages=[
                {
                    "role": "user",
                    "content": f"Using this summary, write a final polished answer:\n\n{summary_text}"
                }
            ]
        )

        return reply