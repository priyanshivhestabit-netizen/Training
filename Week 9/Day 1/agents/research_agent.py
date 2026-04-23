from autogen import AssistantAgent
from config import LLM_CONFIG

class ResearchAgent:
    def __init__(self):
        self.name = "Research Agent"

        self.agent = AssistantAgent(
            name="research_agent",
            system_message="""
You are a research specialist.
Only gather relevant facts about the topic.
Do not summarize.
Do not answer the final user question directly.
Present findings as structured bullet points with key facts, trends, and context.
""",
            llm_config=LLM_CONFIG
        )

    def process(self, query: str) -> str:
        reply = self.agent.generate_reply(
            messages=[
                {
                    "role": "user",
                    "content": f"Research this topic thoroughly: {query}"
                }
            ]
        )

        return reply