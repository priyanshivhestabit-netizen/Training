import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from Week 9 root
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_CONFIG = {
    "config_list": [
        {
            "model": "llama-3.1-8b-instant",
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": GROQ_API_KEY,
        }
    ],
    "temperature": 0.4,
}