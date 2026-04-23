"""
Central LLM caller — Grok API (xAI) with retry + failure recovery.
All agents use this — never call requests directly.
"""
import time
import logging
import requests
from ..config import GROQ_API_URL, GROQ_API_KEY, MODEL, MAX_RETRIES

logger = logging.getLogger(__name__)


def call_llm(system: str, user: str, max_tokens: int = 600) -> str:
    if not GROQ_API_KEY:
        error_msg = (
            "GROK_API_KEY is not set!\n"
            "Please create a .env file with:\n"
            "GROK_API_KEY=your_api_key_here"
        )
        logger.error(error_msg)
        return f"[ERROR] {error_msg}"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"].strip()
            if result:
                logger.info(f"LLM call succeeded (attempt {attempt})")
                return result
        except Exception as e:
            logger.warning(f"LLM attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(15)

    logger.error("All LLM retries exhausted — returning fallback")
    return "[LLM UNAVAILABLE] Could not generate a response after retries."