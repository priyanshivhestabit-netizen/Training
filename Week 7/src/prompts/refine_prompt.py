def get_refine_prompt(question, answer):
    return f"""The following answer to the question "{question}" may be inaccurate or unsupported:

"{answer}"

Please rewrite it to be more conservative and honest.
If you don't have enough information, clearly say so.
Do not add facts you are not sure about.
"""