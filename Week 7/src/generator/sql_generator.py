import ollama
import re
from src.prompts import get_sql_prompt, get_summarize_prompt


def generate_sql(question, schema):
    prompt = get_sql_prompt(question, schema)

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response["message"]["content"].strip()
    return extract_sql(raw)


def extract_sql(text):
    text = re.sub(r"```(?:sql)?", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "").strip()
    if ";" in text:
        text = text[:text.index(";") + 1]
    return text.strip()


def validate_sql(sql):
    sql_upper = sql.upper().strip()
    if not sql_upper:
        return False, "Empty query"
    if not sql_upper.startswith("SELECT"):
        return False, f"Only SELECT queries allowed. Got: {sql_upper[:30]}"
    for word in ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]:
        if word in sql_upper:
            return False, f"Dangerous keyword found: {word}"
    return True, "OK"


def summarize_results(question, sql, columns, rows):
    if not rows:
        return "No data found for your query."

    from src.pipelines.sql_pipeline import format_table
    result_text = format_table(columns, rows)
    prompt = get_summarize_prompt(question, sql, result_text)

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"].strip()