import logging
from nexus_ai.core.llm import call_llm
logger = logging.getLogger(__name__)

class ReporterAgent:
    SYSTEM = """You are a technical report writer.

If the task asks for CODE (e.g. 'write a function', 'give me code', 'implement X'):
- Output the FULL working code block FIRST using markdown triple backticks
- Then add a 3-5 line explanation below
- DO NOT write Executive Summary, Key Findings, or Action Plan for code tasks
- NEVER replace code with descriptions

If the task is non-technical (strategy, planning, analysis):
- Executive Summary
- Key Findings  
- Technical Recommendations
- Action Plan
- Risks & Mitigations"""

    def report(self, task: str, all_outputs: dict) -> str:
        logger.info("[Reporter] generating final report")
        combined = "\n\n".join(f"## {k}\n{v}" for k, v in all_outputs.items())
        return call_llm(
            self.SYSTEM,
            f"Task: {task}\n\nAll agent outputs:\n{combined}",
            max_tokens=800
        )