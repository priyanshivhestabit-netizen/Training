from autogen import AssistantAgent
from config import LLM_CONFIG
class SummarizerAgent:
    def __init__(self):
        self.name = "Summarizer Agent"

        self.agent = AssistantAgent(
            name="summarizer_agent",
            system_message="""
You only summarize research data provided to you.
Do not add new facts or information beyond what is given.
Do not answer the final user question directly.
Produce a clean, concise, well-structured summary of the key points.
""",
            llm_config=LLM_CONFIG
        )

    def process(self, research_text: str) -> str:
        reply = self.agent.generate_reply(
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this research:\n\n{research_text}"
                }
            ]
        )

        return reply