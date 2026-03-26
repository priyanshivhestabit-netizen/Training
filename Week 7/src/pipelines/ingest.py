import os
import json

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import FAISSStore

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

# SAVE CLEANED DATA
def save_cleaned_data(documents):
    os.makedirs("src/data/cleaned",exist_ok=True)
    cleaned=[]
    for doc in documents:
        cleaned.append({
            "text": doc.page_content,
            "metadata": doc.metadata
        })
    with open("src/data/cleaned/cleaned.json","w") as f:
        json.dump(cleaned,f,indent=2)
    print(" Cleaned data saved")

# CHUNK DOCUMENTS
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)

# SAVE CHUNKS
def save_chunks(chunks):
    os.makedirs("src/data/chunks",exist_ok=True)

    chunk_data=[]
    for i,doc in enumerate(chunks):
        chunk_data.append({
            "chunk_id":i,
            "text": doc.page_content,
            "metadata": doc.metadata
        })
    
    with open("src/data/chunks/chunks.json","w") as f:
        json.dump(chunk_data,f,indent=2)

    print("Chunks saved")
    
# MAIN PIPELINE

def main():
    print("Starting ingestion...")

    folder = "src/data/raw"

    docs = load_documents(folder)
    print(f"Loaded documents: {len(docs)}")

    if len(docs) == 0:
        print("No documents found. Add files in src/data/raw/")
        return None
    
    save_cleaned_data(docs)

    chunks = chunk_documents(docs)
    print(f" Created chunks: {len(chunks)}")

    save_chunks(chunks)

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
    store.save()
    print(" INGESTION COMPLETE")

    return store


if __name__ == "__main__":
    main()