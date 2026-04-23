import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import sqlite3
import logging
from rich import print
from rich.table import Table
from rich.panel import Panel
from rich import console as rich_console

from autogen import AssistantAgent
from config import LLM_CONFIG

from tools.file_agent import FileAgent
from tools.code_executor import CodeAgent
from tools.db_agent import DBAgent


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "day3.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

console = rich_console.Console()

DB_SCHEMA = """
Table: reports
Columns:
- id INTEGER
- total_sales INTEGER
- average_sales REAL
- best_month TEXT
- max_sales INTEGER
- total_customers INTEGER
- llm_insights TEXT
"""

# Current loaded CSV state
current_csv_rows = []
current_csv_filename = ""


# ── Shared LLM Helper via AutoGen 

def call_llm(system: str, user: str) -> str:
    agent = AssistantAgent(
        name="helper_agent",
        system_message=system,
        llm_config=LLM_CONFIG
    )

    reply = agent.generate_reply(
        messages=[
            {"role": "user", "content": user}
        ]
    )

    return str(reply).strip()

# ── Intent Detection 
def detect_intent(user_input: str, has_csv: bool) -> str:
    lower = user_input.lower()

    if ".csv" in lower:
        return "load_csv"

    if ".txt" in lower:
        return "load_txt"

    db_keywords = [
        "report", "stored", "db", "database",
        "history", "record", "previous"
    ]

    csv_keywords = [
        "region", "month", "sales", "customer",
        "trend", "highest", "lowest", "average",
        "best", "worst", "total", "compare"
    ]

    if any(k in lower for k in db_keywords):
        return "ask_db"

    if has_csv and any(k in lower for k in csv_keywords):
        return "ask_csv"

    if has_csv:
        return "ask_csv"

    return "ask_db"


# ── NL to SQL 
def nl_to_sql(question: str) -> str:
    return call_llm(
        f"""
You are a SQLite expert.
Convert natural language to SQL SELECT query.
Schema:
{DB_SCHEMA}

Rules:
- Return ONLY SQL
- Only SELECT statements
- No markdown
- No explanation
""",
        f"Convert this to SQL: {question}"
    )

# ── Ask CSV
def answer_csv_question(question: str, rows: list, filename: str) -> str:
    headers = ", ".join(rows[0].keys()) if rows else ""

    data_lines = "\n".join(
        [", ".join(str(v) for v in row.values()) for row in rows[:50]]
    )

    return call_llm(
        """
You are a data analyst.

Answer the user's question using the CSV data.
Use actual values from data.
Be direct and helpful.
""",
        f"""
File: {filename}

Headers:
{headers}

Data:
{data_lines}

Question:
{question}
"""
    )

# ── SQL Runner 
def run_sql(db_path: str, sql: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(sql)

    rows = cur.fetchall()
    columns = [d[0] for d in cur.description] if cur.description else []

    conn.close()

    return columns, rows

# ── Display Helpers 
def display_insights(insights: dict):
    table = Table(title="Sales Analysis", style="bold cyan")
    table.add_column("Metric", style="green")
    table.add_column("Value", style="white")

    table.add_row("Total Sales", str(insights["total_sales"]))
    table.add_row("Average Sales", str(insights["average_sales"]))
    table.add_row("Best Month", insights["best_month"])
    table.add_row("Peak Sales", str(insights["max_sales"]))
    table.add_row("Total Customers", str(insights["total_customers"]))

    console.print(table)

    print("\n[bold magenta]Top 5 Insights[/bold magenta]")

    for i, insight in enumerate(insights.get("insights", []), 1):
        print(f"  [green]{i}.[/green] {insight}")


def display_table(columns, rows):
    if not rows:
        print("[dim]No results found.[/dim]")
        return

    table = Table(style="cyan")

    for col in columns:
        table.add_column(col)

    for row in rows:
        table.add_row(*[str(v) for v in row])

    console.print(table)


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    global current_csv_rows, current_csv_filename

    print("[bold cyan]DAY 3 - Tool Calling Agents[/bold cyan]\n")

    db_path = os.path.join(DATA_DIR, "reports.db")

    file_agent = FileAgent()
    code_agent = CodeAgent()
    db_agent = DBAgent(db_path)

    db_agent.setup()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "bye"):
            print("[bold cyan]Goodbye![/bold cyan]")
            break

        intent = detect_intent(user_input, bool(current_csv_rows))

        # CSV Load
        if intent == "load_csv":
            filename = next((w for w in user_input.split() if ".csv" in w), None)

            if not filename:
                print("[red]CSV filename missing.[/red]")
                continue

            file_path = os.path.join(DATA_DIR, filename)

            rows = file_agent.read_csv(file_path)

            current_csv_rows = rows
            current_csv_filename = filename

            insights = code_agent.analyze_sales(rows)

            llm_text = "\n".join(insights.get("insights", []))

            db_agent.insert_report(insights, llm_text)

            display_insights(insights)

        # TXT Load
        elif intent == "load_txt":
            filename = next((w for w in user_input.split() if ".txt" in w), None)

            file_path = os.path.join(DATA_DIR, filename)

            content = file_agent.read_txt(file_path)

            summary = call_llm(
                "You summarize text clearly.",
                content
            )

            console.print(
                Panel(summary, title=filename)
            )

        # Ask CSV
        elif intent == "ask_csv":
            answer = answer_csv_question(
                user_input,
                current_csv_rows,
                current_csv_filename
            )

            console.print(Panel(answer, title="Answer"))

        # Ask DB
        elif intent == "ask_db":
            try:
                sql = nl_to_sql(user_input)
                columns, rows = run_sql(db_path, sql)
                display_table(columns, rows)

            except Exception as e:
                print(f"[red]Error:[/red] {e}")

        else:
            print("[dim]I didn't understand.[/dim]")


if __name__ == "__main__":
    main()