import logging
from autogen import AssistantAgent
from config import LLM_CONFIG

logger = logging.getLogger(__name__)


class Validator:
    def __init__(self):
        self.name = "Validator Agent"

        self.agent = AssistantAgent(
            name="validator_agent",
            system_message="""
You are a quality validator. You will receive a draft response.

Check it for:
- Completeness: Does it fully address the topic?
- Clarity: Is it easy to understand?
- Accuracy: Does it seem factually reasonable?
- Structure: Is it well organized?

If it passes, respond with:

Validation Passed 

followed by a brief quality note, then the final polished text.

If it fails, respond with:

Validation Failed 

followed by specific reasons why.
""",
            llm_config=LLM_CONFIG
        )

    def validate(self, text):
        try:
            logger.info("Validator checking response")

            if len(text.strip()) < 20:
                return "Validation Failed : Response too short to evaluate."

            reply = self.agent.generate_reply(
                messages=[
                    {
                        "role": "user",
                        "content": f"Validate this response:\n\n{text}"
                    }
                ]
            )

            return str(reply)

        except Exception as e:
            logger.error(f"Validator error: {e}")
            return "Validation failed."