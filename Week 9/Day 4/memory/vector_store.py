import faiss
import numpy as np
import requests
import logging
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
FALLBACK_DIM = 384

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = str(BASE_DIR / "data" / "vector_store.index")
TEXTS_FILE = str(BASE_DIR / "data" / "vector_store_texts.json")


class VectorStore:
    def __init__(self):
        self.dimension = None
        self.index = None
        self.texts = []
        self._load()

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
            vec = np.zeros((1, FALLBACK_DIM), dtype="float32")
            for ch in text:
                vec[0][ord(ch) % FALLBACK_DIM] += 1
            return vec

    def _init_index(self, dim: int):
        self.dimension = dim
        self.index = faiss.IndexFlatL2(dim)
        logger.info(f"FAISS index initialized with dim={dim}")

    def _save(self):
        Path(os.path.dirname(INDEX_FILE)).mkdir(parents=True, exist_ok=True)
        if self.index is not None:
            faiss.write_index(self.index, INDEX_FILE)
        with open(TEXTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.texts, f, ensure_ascii=False, indent=2)
        logger.info("Vector store saved to disk")

    def _load(self):
        Path(os.path.dirname(INDEX_FILE)).mkdir(parents=True, exist_ok=True)
        if os.path.exists(INDEX_FILE):
            self.index = faiss.read_index(INDEX_FILE)
            self.dimension = self.index.d
            logger.info("Loaded FAISS index from disk")
        if os.path.exists(TEXTS_FILE):
            with open(TEXTS_FILE, "r", encoding="utf-8") as f:
                self.texts = json.load(f)
            logger.info(f"Loaded {len(self.texts)} texts from disk")

    def add(self, text: str):
        vec = self._get_embedding(text)
        if self.index is None:
            self._init_index(vec.shape[1])
        self.index.add(vec)
        self.texts.append(text)
        self._save()
        logger.info(f"Added to vector store: {text[:60]}")

    def search(self, query: str, top_k: int = 2):
        if self.index is None or not self.texts:
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
