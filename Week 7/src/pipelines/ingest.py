import os
import faiss
import numpy as np

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# LOAD DOCUMENTS

def load_documents(folder):
    docs = []

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        try:
            if file.endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif file.endswith(".txt"):
                loader = TextLoader(path)
            else:
                continue

            loaded_docs = loader.load()

            # Add source metadata manually
            for d in loaded_docs:
                d.metadata["source"] = file

            docs.extend(loaded_docs)

        except Exception as e:
            print(f"Error loading {file}: {e}")

    return docs

# CHUNK DOCUMENTS
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)

# EMBEDDINGS
model = SentenceTransformer("BAAI/bge-small-en")

def embed_texts(texts):
    return model.encode(texts)

# FAISS STORE
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

# MAIN PIPELINE

def main():
    print("Starting ingestion...")

    folder = "src/data/raw"

    docs = load_documents(folder)
    print(f"Loaded documents: {len(docs)}")

    if len(docs) == 0:
        print("No documents found. Add files in src/data/raw/")
        return None

    chunks = chunk_documents(docs)
    print(f" Created chunks: {len(chunks)}")

    texts = []
    metadata = []

    for i, doc in enumerate(chunks):
        texts.append(doc.page_content)
        metadata.append({
            "source": doc.metadata.get("source", "unknown"),
            "chunk": i
        })

    embeddings = embed_texts(texts)
    print(" Embeddings created")

    dim = len(embeddings[0])
    store = FAISSStore(dim)
    store.add(embeddings, texts, metadata)

    print(" Stored in FAISS")
    print(" INGESTION COMPLETE")

    return store


if __name__ == "__main__":
    main()