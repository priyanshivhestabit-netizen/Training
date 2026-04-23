"""
Natural Language Query Interface for nexus_memory.db
Usage: python query_memory.py
"""
import os
import sqlite3
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL        = "llama-3.1-8b-instant"
DB_PATH      = "data/nexus_memory.db"

SCHEMA = """
Table: memories
Columns:
  - id         INTEGER  (auto increment primary key)
  - category   TEXT     (values: 'system', 'task', 'output', 'code')
  - text       TEXT     (the actual memory content)
  - created_at TIMESTAMP (e.g. '2026-04-21 07:41:36')
"""

SYSTEM_PROMPT = f"""You are a SQLite expert. Convert natural language questions into SQL queries.

Database schema:
{SCHEMA}

Rules:
- Return ONLY the raw SQL query, nothing else
- No markdown, no backticks, no explanation
- Always use SELECT (never DELETE or DROP)
- Use LIKE '%keyword%' for text searches
- Use substr(text, 1, 150) to truncate long text in results
- Failures contain 'failed' or 'UNAVAILABLE' in text
- Successful outputs do NOT contain 'failed' or 'UNAVAILABLE'
"""

def text_to_sql(question: str) -> str:
    response = requests.post(GROQ_API_URL, headers={
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Convert to SQL: {question}"}
        ],
        "max_tokens": 200,
        "temperature": 0.1
    }, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def run_query(sql: str):
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute(sql)
    rows    = cur.fetchall()
    columns = [d[0] for d in cur.description] if cur.description else []
    conn.close()
    return columns, rows

def display(columns, rows):
    if not rows:
        print("  No results found.")
        return
    print(f"  {len(rows)} row(s) returned\n")
    col_str = " | ".join(f"{c:<20}" for c in columns)
    print("  " + col_str)
    print("  " + "-" * len(col_str))
    for row in rows:
        print("  " + " | ".join(f"{str(v):<20}" for v in row))

def main():
    print("\n" + "="*60)
    print("  NEXUS AI — Memory Query Interface")
    print("  Ask questions in plain English about your memory DB")
    print("  Type 'exit' to quit")
    print("="*60 + "\n")

    while True:
        question = input("Ask: ").strip()
        if not question:
            continue
        if question.lower() in ("exit", "quit"):
            break

        try:
            print("\n  Generating SQL...")
            sql = text_to_sql(question)
            print(f"  SQL: {sql}\n")

            columns, rows = run_query(sql)
            display(columns, rows)

        except sqlite3.Error as e:
            print(f"  SQL Error: {e}")
            print("  Try rephrasing your question.")
        except Exception as e:
            print(f"  Error: {e}")

        print()

if __name__ == "__main__":
    main()