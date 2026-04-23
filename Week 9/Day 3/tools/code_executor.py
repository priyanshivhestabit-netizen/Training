import logging
import json
from autogen import AssistantAgent
from config import LLM_CONFIG

logger = logging.getLogger(__name__)


class CodeAgent:
    def __init__(self):
        self.name = "Code Agent"

        self.agent = AssistantAgent(
            name="code_agent",
            system_message="""
You are a data analyst. You will receive raw CSV data as text.

Your job is to:
1. Compute basic stats (total, average, min, max, trends)
2. Generate the top 5 actionable business insights
3. Return ONLY a valid JSON object with exactly these keys:

- total_sales (int)
- average_sales (float)
- best_month (str)
- max_sales (int)
- total_customers (int)
- insights (list of 5 strings)

No explanation.
No markdown.
Just raw JSON.
""",
            llm_config=LLM_CONFIG
        )

    def analyze_sales(self, rows: list[dict]) -> dict:
        try:
            logger.info("CodeAgent analyzing sales data via AutoGen")

            # Convert rows to CSV text
            headers = ",".join(rows[0].keys())
            data_lines = "\n".join(
                [",".join(str(v) for v in row.values()) for row in rows]
            )
            csv_text = f"{headers}\n{data_lines}"

            reply = self.agent.generate_reply(
                messages=[
                    {
                        "role": "user",
                        "content": f"Analyze this sales data:\n\n{csv_text}"
                    }
                ]
            )

            raw = str(reply).strip()

            # Extract JSON safely
            start = raw.find("{")
            end = raw.rfind("}") + 1
            result = json.loads(raw[start:end])

            logger.info("CodeAgent analysis complete")
            return result

        except Exception as e:
            logger.error(f"CodeAgent error: {e}")

            # Fallback deterministic stats
            sales = [int(r["sales"]) for r in rows]
            customers = [int(r["customers"]) for r in rows]

            return {
                "total_sales": sum(sales),
                "average_sales": round(sum(sales) / len(sales), 2),
                "best_month": rows[sales.index(max(sales))]["month"],
                "max_sales": max(sales),
                "total_customers": sum(customers),
                "insights": [
                    "LLM unavailable - basic stats computed as fallback.",
                    "Highest sales month identified.",
                    "Average sales calculated.",
                    "Customer totals aggregated.",
                    "Consider deeper trend analysis."
                ]
            }