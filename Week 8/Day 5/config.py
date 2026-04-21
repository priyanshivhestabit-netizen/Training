import os

MODEL_CONFIG = {
    "mode": os.getenv("MODE", "gguf"),
    "base_model": os.getenv("BASE_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0"),
    "adapter_path": os.getenv("ADAPTER_PATH", "../Day2/adapters"),
    "gguf_path": os.getenv("GGUF_PATH", "Day 3/quantized/model.gguf"),
    "quantization": os.getenv("QUANTIZATION", "gguf"),
}

GENERATION_DEFAULTS = {
    "max_new_tokens": 256,      # Default max output length
    "temperature": 0.7,          # 0=deterministic, 1=creative, >1=random
    "top_p": 0.9,               # Nucleus sampling: top p% probability mass
    "top_k": 50,                # Keep only top k tokens at each step
    "repetition_penalty": 1.1,  # Penalize repeated words (1.0=none, >1.0=penalize)
    "do_sample": True,          # True=sample, False=greedy
}

SERVER_CONFIG = {
    "host": os.getenv("HOST", "0.0.0.0"),
    "port": int(os.getenv("PORT", "8000")),
    "workers": int(os.getenv("WORKERS", "1")),
    "log_level": os.getenv("LOG_LEVEL", "info"),
}

PROMPT_TEMPLATES = {
    "alpaca": {
        "with_input": (
            "### Instruction:\n{instruction}\n\n"
            "### Input:\n{input}\n\n"
            "### Response:\n"
        ),
        "without_input": (
            "### Instruction:\n{instruction}\n\n"
            "### Response:\n"
        ),
    },
    "chat": {
        "system": "You are a helpful financial assistant. Provide accurate, concise answers.",
        "user_prefix": "User: ",
        "assistant_prefix": "Assistant: ",
    },
}

# ─── System Prompts ───────────────────────────────────────────────────────────
SYSTEM_PROMPTS = {
    "deafult":"You are a professional financial advisor AI. Provide clear, accurate financial information. Always note when professional advice should be sought.",
}

# ─── Limits ───────────────────────────────────────────────────────────────────
LIMITS = {
    "max_prompt_length": 1000,    # Characters
    "max_chat_history": 10,       # Number of turns to keep in memory
    "rate_limit_per_minute": 30,  # Requests per minute (basic rate limiting)
}