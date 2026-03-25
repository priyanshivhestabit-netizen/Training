# GenAI RAG System - Day 1

## Features
- Document ingestion (PDF, TXT)
- Chunking (800 tokens, overlap 100)
- Embeddings using BGE-small
- FAISS vector database
- Semantic retrieval with metadata (source, chunk)

## How to Run

```bash
python -m src.retriever.query_engine