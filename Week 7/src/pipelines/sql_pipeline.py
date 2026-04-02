import sqlite3
import ollama
from src.utils.schema_loader import get_schema, get_sample_rows
from src.generator.sql_generator import generate_sql, validate_sql

DB_PATH = "src/data/database/enterprise.db"


def execute_sql(sql, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    conn.close()
    return columns, rows


def format_table(columns, rows):
    if not rows:
        return "No results found."

    # Build header
    col_widths = [max(len(str(c)), max(len(str(r[i])) for r in rows))
                  for i, c in enumerate(columns)]

    header = " | ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(columns))
    separator = "-+-".join("-" * w for w in col_widths)

    lines = [header, separator]
    for row in rows:
        line = " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row))
        lines.append(line)

    return "\n".join(lines)


def summarize_results(question, sql, columns, rows):
    if not rows:
        return "No data found for your query."

    # Format results for LLM
    result_text = format_table(columns, rows)

    prompt = f"""A user asked: "{question}"
We ran this SQL query: {sql}

The result was:
{result_text}

Write a short, clear 2-3 sentence summary of these results in plain English.
Focus on key insights — highest/lowest values, totals, patterns.
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()


def run_sql_qa(question, db_path=DB_PATH):
    print(f"\nQuestion: {question}")

    # Step 1: Schema
    schema = get_schema(db_path)

    # Step 2: Generate SQL
    print("Generating SQL...")
    sql = generate_sql(question, schema)
    print(f"Generated SQL: {sql}")

    # Step 3: Validate
    valid, msg = validate_sql(sql)
    if not valid:
        return {
            "question": question,
            "sql": sql,
            "error": msg,
            "results": None,
            "summary": f"Could not execute query: {msg}"
        }

    # Step 4: Execute
    try:
        print("Executing SQL...")
        columns, rows = execute_sql(sql, db_path)
        table = format_table(columns, rows)
        print(f"Results:\n{table}")
    except Exception as e:
        return {
            "question": question,
            "sql": sql,
            "error": str(e),
            "results": None,
            "summary": f"SQL execution error: {e}"
        }

    # Step 5: Summarize
    print("Summarizing...")
    summary = summarize_results(question, sql, columns, rows)

    return {
        "question": question,
        "sql": sql,
        "columns": columns,
        "rows": rows,
        "table": table,
        "summary": summary,
        "error": None
    }


def run():
    print("\n")
    print("  SQL QUESTION ANSWERING SYSTEM")
    print("="*55)
    print("  Ask questions in plain English about the database.")
    print("  Type 'schema' to see DB structure.")
    print("  Type 'exit' to quit.")
    print("="*55 + "\n")

    while True:
        question = input("Ask a question: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            print("Bye!")
            break

        if question.lower() == "schema":
            print(get_schema())
            print(get_sample_rows())
            continue

        result = run_sql_qa(question)

        print("\n" + "="*55)
        print(f"SQL     : {result['sql']}")
        if result["error"]:
            print(f"ERROR   : {result['error']}")
        else:
            print(f"RESULTS :\n{result['table']}")
        print(f"\nSUMMARY : {result['summary']}")
        print("="*55 + "\n")


if __name__ == "__main__":
    run()