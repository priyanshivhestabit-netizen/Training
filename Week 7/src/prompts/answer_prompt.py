def get_answer_prompt(question, context_text, conversation_history=""):
    return f"""You are a helpful enterprise assistant.

Previous conversation:
{conversation_history}

Context from documents:
{context_text}

Answer this question based ONLY on the context above:
"{question}"

If the answer is not in the context, say "I don't have enough information."
Keep the answer concise and factual.
"""