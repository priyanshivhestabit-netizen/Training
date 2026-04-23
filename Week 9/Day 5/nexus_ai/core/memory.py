"""
Unified memory interface: session + long-term SQLite + FAISS vector store.
"""
import sqlite3
import logging
import numpy as np
import requests
import faiss
from collections import deque
from nexus_ai.config import EMBED_URL, EMBED_MODEL, MEMORY_DB, SESSION_LIMIT, TOP_K_RECALL

logger = logging.getLogger(__name__)
FALLBACK_DIM = 384


class SessionMemory:
    def __init__(self):
        self.history = deque(maxlen=SESSION_LIMIT)

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def format(self) -> str:
        return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in self.history)

    def last_n(self, n: int = 4) -> str:
        items = list(self.history)[-n:]
        return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in items)


class LongTermMemory:
    def __init__(self):
        self.db_path = MEMORY_DB
        self.setup()

    def setup(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                category   TEXT,
                text       TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit(); conn.close()

    def store(self, text: str, category: str = "general"):
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO memories(category, text) VALUES (?,?)", (category, text))
        conn.commit(); conn.close()
        logger.info(f"[LongTerm] stored ({category}): {text[:60]}")

    def fetch_by_category(self, category: str):
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT text FROM memories WHERE category=? ORDER BY created_at DESC LIMIT 10",
            (category,)
        ).fetchall()
        conn.close()
        return [r[0] for r in rows]


class VectorStore:
    def __init__(self):
        self.index = None
        self.texts = []
        self.dim   = None

    def _embed(self, text: str) -> np.ndarray:
        try:
            r = requests.post(EMBED_URL, json={"model": EMBED_MODEL, "prompt": text}, timeout=30)
            r.raise_for_status()
            return np.array([r.json()["embedding"]], dtype="float32")
        except Exception as e:
            logger.warning(f"Embedding fallback: {e}")
            vec = np.zeros((1, FALLBACK_DIM), dtype="float32")
            for ch in text:
                vec[0][ord(ch) % FALLBACK_DIM] += 1
            return vec

    def add(self, text: str):
        vec = self._embed(text)
        if self.index is None:
            self.dim   = vec.shape[1]
            self.index = faiss.IndexFlatL2(self.dim)
        self.index.add(vec)
        self.texts.append(text)

    def search(self, query: str, top_k: int = TOP_K_RECALL):
        if not self.texts:
            return []
        vec = self._embed(query)
        k   = min(top_k, len(self.texts))
        _, idxs = self.index.search(vec, k)
        return [self.texts[i] for i in idxs[0] if 0 <= i < len(self.texts)]