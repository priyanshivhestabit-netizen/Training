def get_sql_prompt(question, schema):
    return f"""You are an expert SQL writer for SQLite databases.

Here is the database schema:
{schema}

Write a single valid SQLite SQL query to answer this question:
"{question}"

Rules:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no backticks
- Use only tables and columns that exist in the schema above
- End the query with a semicolon
"""