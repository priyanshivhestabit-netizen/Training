import faiss
import numpy as np
import requests
import logging

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
EMBED_MODEL = "nomic-embed-text"  # best local embedding model via Ollama
FALLBACK_DIM = 384


class VectorStore:
    def __init__(self):
        self.dimension = None
        self.index = None
        self.texts = []

    def _get_embedding(self, text: str) -> np.ndarray:
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": EMBED_MODEL,
                "prompt": text
            })
            response.raise_for_status()
            embedding = response.json()["embedding"]
            return np.array([embedding], dtype="float32")
        except Exception as e:
            logger.warning(f"Embedding model failed, using fallback: {e}")
            # Fallback: deterministic char-frequency vector
            vec = np.zeros((1, FALLBACK_DIM), dtype="float32")
            for i, ch in enumerate(text):
                vec[0][ord(ch) % FALLBACK_DIM] += 1
            return vec

    def _init_index(self, dim: int):
        self.dimension = dim
        self.index = faiss.IndexFlatL2(dim)
        logger.info(f"FAISS index initialized with dim={dim}")

    def add(self, text: str):
        vec = self._get_embedding(text)
        if self.index is None:
            self._init_index(vec.shape[1])
        self.index.add(vec)
        self.texts.append(text)
        logger.info(f"Added to vector store: {text[:60]}")

    def search(self, query: str, top_k: int = 2):
        if not self.texts:
            return []
        vec = self._get_embedding(query)
        top_k = min(top_k, len(self.texts))
        distances, indices = self.index.search(vec, top_k)
        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.texts):
                results.append(self.texts[idx])
        logger.info(f"Vector search returned {len(results)} results")
        return results