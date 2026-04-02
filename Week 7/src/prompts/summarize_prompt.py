def get_summarize_prompt(question, sql, result_text):
    return f"""A user asked: "{question}"
We ran this SQL query: {sql}

The result was:
{result_text}

Write a short, clear 2-3 sentence summary of these results in plain English.
Focus on key insights — highest/lowest values, totals, patterns.
"""