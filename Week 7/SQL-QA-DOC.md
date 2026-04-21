# SQL QUESTION ANSWERING

## Overview

The SQL QA pipeline converts a plain-English question into a SQL query, executes it safely against a SQLite database, and uses Mistral to summarise the results in natural language. The user never writes SQL — the LLM generates it, a validator checks it, and the result is returned as both a table and a prose summary.

---

## Full Pipeline

```
User question (plain English)
        │
        ▼
get_schema(db_path)          ← reads all table names, columns, types from SQLite
        │
        ▼
generate_sql(question, schema)
    └── get_sql_prompt()     ← builds the prompt with schema + question
    └── ollama.chat()        ← Mistral generates raw SQL
    └── extract_sql()        ← strips markdown fences, truncates at semicolon
        │
        ▼
validate_sql(sql)
    ├── must start with SELECT
    └── must not contain DROP / DELETE / UPDATE / INSERT / ALTER / TRUNCATE
        │
        ▼ (if valid)
execute_sql(sql, db_path)
    └── sqlite3.connect()
    └── cursor.execute()
    └── cursor.fetchall()    ← returns columns + rows
        │
        ▼
format_table(columns, rows)  ← aligned ASCII table for display
        │
        ▼
summarize_results(question, sql, columns, rows)
    └── ollama.chat()        ← Mistral writes 2–3 sentence plain English summary
        │
        ▼
Return: { question, sql, columns, rows, table, summary, error }
```

---

## Component 1 — Schema Loading

### What it does

Before asking the LLM to generate SQL, the pipeline reads the complete database schema and passes it to Mistral as context. Without the schema, the LLM would have to guess table and column names, producing SQL that references non-existent tables.

### Implementation (in `schema_loader.py`)

```python
def get_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    # for each table: PRAGMA table_info(table_name) → column names and types
```

`sqlite_master` is SQLite's internal metadata table. `type='table'` filters out views, triggers, and indexes. `PRAGMA table_info(name)` returns one row per column with: column index, name, data type, not-null constraint, default value, and whether it is a primary key.

---

## Component 2 — SQL Generation (`sql_generator.py`)

### Prompt construction

```python
def generate_sql(question, schema):
    prompt = get_sql_prompt(question, schema)
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    raw = response["message"]["content"].strip()
    return extract_sql(raw)
```

The prompt (defined in `src/prompts.py`) gives Mistral the database schema and asks it to return only the SQL query with no explanation. Instructing the model to return only SQL is important — if it returns "Here is the query: SELECT..." the extraction step strips the preamble, but shorter model output is cheaper and faster.

### SQL extraction

```python
def extract_sql(text):
    text = re.sub(r"```(?:sql)?", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "").strip()
    if ";" in text:
        text = text[:text.index(";") + 1]
    return text.strip()
```

LLMs frequently wrap code in markdown fences like ` ```sql ... ``` `. The regex removes the opening fence with optional language tag. The second replace handles the closing fence. The semicolon logic keeps only the first SQL statement — important because some LLMs append a second example query or explanation after the semicolon.

`re.IGNORECASE` handles cases where the model writes ` ```SQL ` with an uppercase tag.

---

## Component 3 — SQL Validation (`sql_generator.py`)

### Why validation is mandatory

Without validation, a prompt-injected question like "drop the users table then show me sales" could cause Mistral to generate `DROP TABLE users; SELECT * FROM sales`. Executing that would silently delete your data.

### The validator

```python
def validate_sql(sql):
    sql_upper = sql.upper().strip()
    if not sql_upper:
        return False, "Empty query"
    if not sql_upper.startswith("SELECT"):
        return False, f"Only SELECT queries allowed."
    for word in ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]:
        if word in sql_upper:
            return False, f"Dangerous keyword found: {word}"
    return True, "OK"
```

The whitelist approach (`startswith("SELECT")`) is the primary defence. The blacklist (`DROP`, `DELETE`, etc.) is a secondary check for edge cases — for example, a subquery that begins with SELECT but contains a DELETE inside a CTE. Both checks together provide strong protection for a read-only use case.

### What it does not protect against

SQL injection via string literals is not guarded here because the LLM generates the query rather than a user typing raw SQL values. However, if you later add support for parameterised user inputs directly in SQL, always use parameterised queries (`cursor.execute("SELECT * FROM t WHERE id = ?", [user_id])`) rather than string formatting.

---

## Component 4 — Execution (`sql_pipeline.py`)

```python
def execute_sql(sql, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return columns, rows
```

`sqlite3.connect()` opens the database file. For read-only access you could open it with `uri=True` and append `?mode=ro` to the path, which prevents any write even if validation is bypassed. This is a recommended hardening step.

`cursor.description` is a sequence of 7-item tuples. Index 0 is always the column name. The other six items (type_code, display_size, internal_size, precision, scale, null_ok) are present for DB-API 2.0 compliance but SQLite sets most of them to `None`.

`cursor.fetchall()` loads all result rows into memory. For very large result sets this could be a memory issue. `cursor.fetchmany(n)` or `cursor.fetchone()` in a loop would be safer for production use.

`conn.close()` releases the file lock. Without this, repeated calls would accumulate open file handles. Using `with sqlite3.connect(db_path) as conn:` (context manager) would close it automatically even on exceptions.

---

## Component 5 — Table Formatting (`sql_pipeline.py`)

```python
def format_table(columns, rows):
    col_widths = [max(len(str(c)), max(len(str(r[i])) for r in rows))
                  for i, c in enumerate(columns)]
    header = " | ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(columns))
    separator = "-+-".join("-" * w for w in col_widths)
    lines = [header, separator]
    for row in rows:
        line = " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row))
        lines.append(line)
    return "\n".join(lines)
```

For each column, `col_widths[i]` is the maximum of: the column header's character count, and the longest value in that column. `str(c).ljust(width)` left-justifies the string, padding with spaces to `width` characters. The result is a monospaced table readable in any terminal or fixed-width font context.

### Example output

```
name          | revenue | region
--------------+---------+--------
Acme Corp     | 2400000 | West
Beta Ltd      | 980000  | East
```

This is passed both to the Streamlit UI (in the "Raw Results" expander) and to Mistral as context for the summary.

---

## Component 6 — Natural Language Summary

### In `sql_pipeline.py`

```python
def summarize_results(question, sql, columns, rows):
    result_text = format_table(columns, rows)
    prompt = f"""A user asked: "{question}"
We ran this SQL query: {sql}
The result was:
{result_text}
Write a short, clear 2-3 sentence summary..."""
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()
```

### Duplication issue

`summarize_results` is defined in both `sql_pipeline.py` and `sql_generator.py`. The `sql_generator.py` version imports `format_table` from `sql_pipeline.py` and is never called anywhere in the codebase. **Delete the version in `sql_generator.py` entirely.** The working version is in `sql_pipeline.py`.

---

## The `/ask-sql` Endpoint (`app.py`)

```python
@app.post("/ask-sql")
def ask_sql(req: SqlAskRequest):
    result = run_sql_qa(req.question)
    memory.add("user", req.question, "/ask-sql")
    memory.add("assistant", result["summary"], "/ask-sql")
    return {
        "question": req.question,
        "sql": result["sql"],
        "table": result.get("table", ""),
        "summary": result["summary"],
        "error": result.get("error")
    }
```

The SQL endpoint does not use `memory.get_context()` when generating SQL — conversation history is not passed to the SQL generator. This is intentional: SQL generation is stateless by design. Passing prior Q&A into the SQL prompt would confuse Mistral and often produce incorrect queries. The memory is only stored after the fact for display in the sidebar.

---

## Streamlit Display (`streamlit_app.py`)

```python
elif "SQL QA" in mode:
    res = requests.post(f"{API_URL}/ask-sql", json={"question": question}).json()
    if res.get("error"):
        st.error(f"SQL Error: {res['error']}")
    else:
        st.markdown(res.get("summary", ""))
        with st.expander("🔍 Generated SQL"):
            st.code(res.get("sql", ""), language="sql")
        with st.expander("📋 Raw Results"):
            st.text(res.get("table", ""))
```

`st.expander()` creates a collapsible section — appropriate for SQL and raw table data which many users will not need. `st.code()` renders the SQL with syntax highlighting. `st.text()` renders the ASCII table in a monospaced font, preserving the column alignment produced by `format_table`.

---

## Error Handling

The pipeline returns structured errors rather than raising exceptions wherever possible:

| Stage | Error type | Handling |
|-------|-----------|----------|
| Schema loading | File not found, permission error | Exception propagates to `/ask-sql`, returns 500 |
| SQL generation | Ollama not running | `ConnectionError` from `ollama.chat()`, returns 500 |
| SQL extraction | LLM returns empty or non-SQL text | `extract_sql` returns empty string |
| SQL validation | Empty query or non-SELECT | Returns `{"error": msg, "summary": "Could not execute..."}` |
| SQL execution | Syntax error, missing table, type mismatch | Caught by `except Exception as e`, error returned in response |
| Summarisation | Ollama not running | Exception propagates |

The frontend checks `res.get("error")` and displays it with `st.error()` rather than crashing.

---

## Database Setup

The database path is hardcoded:

```python
DB_PATH = "src/data/database/enterprise.db"
```

This SQLite file must exist before the SQL pipeline can run. Create it with your schema and data using the `sqlite3` command-line tool or a Python script. The schema loader reads whatever tables exist — no configuration beyond the file path is needed.

---

## Files Involved

| File | Role |
|------|------|
| `src/utils/schema_loader.py` | Reads SQLite schema for prompt context |
| `src/generator/sql_generator.py` | LLM SQL generation, extraction, validation |
| `src/pipelines/sql_pipeline.py` | Execution, formatting, summarisation, orchestration |
| `src/deployment/app.py` | `/ask-sql` endpoint |
| `src/deployment/streamlit_app.py` | SQL mode UI with SQL and table expanders |