import logging
import json
import io
import contextlib
import traceback
from autogen import AssistantAgent
from config import LLM_CONFIG

logger = logging.getLogger(__name__)


class CodeAgent:
    def __init__(self):
        self.name = "Code Agent"

        self.analyst = AssistantAgent(
            name="data_analyst",
            system_message="""
You are a Python code generator for data analysis.

When given CSV data, write a Python script that:
1. Parses the CSV from a variable called `csv_text` (already defined)
2. Computes: total_sales, average_sales, best_month, max_sales, total_customers
3. Generates 5 actionable business insights as a list of strings
4. Ends with: print(json.dumps(result))

Rules:
- Use only stdlib: csv, json, io, statistics
- Store final output in a dict called `result` with exactly these keys:
  total_sales (int), average_sales (float), best_month (str),
  max_sales (int), total_customers (int), insights (list of 5 strings)
- Do NOT use f-strings with backslashes
- Return ONLY the raw Python code, no markdown, no explanation
""",
            llm_config=LLM_CONFIG
        )

        self.coder = AssistantAgent(
            name="code_generator",
            system_message="""
You are an expert programmer. When the user asks for code:
- Write clean, well-commented code in the requested language (default Python)
- Include a brief docstring or comment block explaining what the code does
- Include example usage at the bottom in an if __name__ == '__main__' block (for Python) or equivalent
- Return ONLY the raw code, no markdown fences, no explanation outside the code
""",
            llm_config=LLM_CONFIG
        )


    def _build_csv_text(self, rows: list[dict]) -> str:
        headers = ",".join(rows[0].keys())
        data_lines = "\n".join(
            ",".join(str(v) for v in row.values()) for row in rows
        )
        return f"{headers}\n{data_lines}"

    def _extract_code(self, reply: str) -> str:
        """Strip markdown fences if the LLM ignores our instructions."""
        raw = reply.strip()
        if "```" in raw:
            raw = raw.split("```", 1)[1]
            
            first_line = raw.split("\n", 1)[0].strip()
            if first_line and not first_line.startswith(("#", "//", "import", "def", "class", "#include")):
                raw = raw.split("\n", 1)[1]
            raw = raw.split("```", 1)[0]
        return raw.strip()

    def _execute_code(self, code: str, csv_text: str) -> dict:
        """Execute generated analysis code and capture printed JSON output."""
        import json as _json

        namespace = {"csv_text": csv_text, "json": _json}
        stdout_capture = io.StringIO()

        with contextlib.redirect_stdout(stdout_capture):
            exec(compile(code, "<generated>", "exec"), namespace)  # noqa: S102

        output = stdout_capture.getvalue().strip()
        last_line = [ln for ln in output.splitlines() if ln.strip()][-1]
        return _json.loads(last_line)

    def _fallback_stats(self, rows: list[dict]) -> dict:
        sales = [int(r["sales"]) for r in rows]
        customers = [int(r["customers"]) for r in rows]
        best_idx = sales.index(max(sales))
        return {
            "total_sales": sum(sales),
            "average_sales": round(sum(sales) / len(sales), 2),
            "best_month": rows[best_idx]["month"],
            "max_sales": max(sales),
            "total_customers": sum(customers),
            "insights": [
                "LLM unavailable — basic stats computed as fallback.",
                "Highest sales month identified from raw data.",
                "Average sales calculated across all months.",
                "Customer totals aggregated from all rows.",
                "Consider re-running with LLM access for deeper insights.",
            ],
        }

    def _detect_language(self, query: str) -> str:
        """Best-effort language detection from the user's query string."""
        q = query.lower()
        languages = {
            "c++":        ["c++", "cpp", "in cpp", "in c++"],
            "c":          [" in c ", "in c,", "c language"],
            "python":     ["python", ".py"],
            "javascript": ["javascript", "js", "node"],
            "typescript": ["typescript", "ts"],
            "java":       [" java ", "in java"],
            "go":         ["golang", " in go"],
            "rust":       ["rust"],
            "sql":        ["sql"],
            "bash":       ["bash", "shell", " sh "],
        }
        for lang, keywords in languages.items():
            if any(kw in q for kw in keywords):
                return lang
        return "python"


    def analyze_sales(self, rows: list[dict]) -> dict:
        """
        Generate + execute Python analysis code for CSV rows.

        Returns:
            {
                "stats": { total_sales, average_sales, ... },
                "code":  "generated python code string" | None
            }
        """
        try:
            logger.info("CodeAgent: analyzing sales data")
            csv_text = self._build_csv_text(rows)

            reply = self.analyst.generate_reply(
                messages=[{
                    "role": "user",
                    "content": (
                        "Write Python code to analyze this sales data.\n\n"
                        f"The variable `csv_text` is already defined as:\n\n{csv_text}"
                    ),
                }]
            )

            code = self._extract_code(str(reply))
            logger.debug("Generated analysis code:\n%s", code)

            stats = self._execute_code(code, csv_text)
            logger.info("CodeAgent: analysis complete")
            return stats

        except Exception as e:
            logger.error("CodeAgent analyze_sales error: %s\n%s", e, traceback.format_exc())
            return {"stats": self._fallback_stats(rows), "code": None}

    def generate_code(self, query: str) -> dict:
        """
        Generate code for any user request.

        Args:
            query: e.g. "give me binary search in Python" or "code for bubble sort in cpp"

        Returns:
            {
                "code":     "generated code string",
                "language": "python" | "c++" | ...,
                "success":  True | False
            }
        """
        try:
            logger.info("CodeAgent: generating code for — %s", query)

            reply = self.coder.generate_reply(
                messages=[{"role": "user", "content": query}]
            )

            code = self._extract_code(str(reply))
            language = self._detect_language(query)

            logger.info("CodeAgent: code generation complete (%s)", language)
            return {"code": code, "language": language, "success": True}

        except Exception as e:
            logger.error("CodeAgent generate_code error: %s\n%s", e, traceback.format_exc())
            return {
                "code": f"# Code generation failed: {e}",
                "language": "unknown",
                "success": False,
            }

    def run(self, query: str = None, rows: list[dict] = None) -> dict:
        """
        Unified entry point — routes to the right handler automatically.

        Usage:
            agent.run(rows=csv_rows)          # sales analysis
            agent.run(query="binary search")  # code generation
        """
        if rows is not None:
            return self.analyze_sales(rows)

        if query is not None:
            return self.generate_code(query)

        raise ValueError("Provide at least one of: `query` or `rows`")