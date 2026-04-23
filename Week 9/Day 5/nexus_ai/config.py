import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

APP_NAME = "NEXUS AI"
VERSION  = "1.0"

# ── Grok API
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("XAI_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL        = "llama-3.1-8b-instant" 

LLM_CONFIG = {
    "config_list": [
        {
            "model": MODEL,
            "api_key": GROQ_API_KEY,
            "base_url": GROQ_API_URL,
        }
    ],
    "temperature": 0.7,
    "timeout": 60,
}

# ── Embeddings 
EMBED_URL   = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"

MAX_RETRIES   = 3
MIN_VALID_LEN = 80
BASE_DIR = Path(__file__).resolve().parent.parent   # Day 5/
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

MEMORY_DB = str(DATA_DIR / "nexus_memory.db")
LOG_FILE = str(LOG_DIR / "day5.log")
TOP_K_RECALL  = 1
SESSION_LIMIT = 20

# Validation
if not GROQ_API_KEY:
    print("  WARNING: GROQ_API_KEY not found!")
    print(f"   Looking for .env at: {env_path}")
    print("   Please create .env file with: GROQ_API_KEY=your_key_here")