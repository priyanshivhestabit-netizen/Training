import faiss
import numpy as np
import os
import json

class FAISSStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.data = []

    def add(self, embeddings, texts, metadata):
        self.index.add(np.array(embeddings))

        for t, m in zip(texts, metadata):
            self.data.append({
                "text": t,
                "source": m["source"],
                "chunk": m["chunk"]
            })

    def search(self, query_embedding, k=5):
        D, I = self.index.search(query_embedding, k)

        results = []
        for idx in I[0]:
            if idx < len(self.data):
                results.append(self.data[idx])

        return results

    def save(self, path="src/vectorstore"):
        os.makedirs(path, exist_ok=True)

        faiss.write_index(self.index, f"{path}/index.faiss")

        with open(f"{path}/metadata.json", "w") as f:
            json.dump(self.data, f)

        print("FAISS saved to disk")

    @classmethod
    def load(cls, path="src/vectorstore"):
        index = faiss.read_index(f"{path}/index.faiss")

        with open(f"{path}/metadata.json", "r") as f:
            data = json.load(f)

        store = cls(index.d)
        store.index = index
        store.data = data

        print("FAISS loaded from disk")

        return store