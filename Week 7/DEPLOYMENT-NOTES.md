# DEPLOYMENT NOTES

## How to Run

### Terminal 1 — Start API server:
```bash
uvicorn src.deployment.app:app --reload --port 8000
```

### Terminal 2 — Start UI:
```bash
streamlit run src/ui/streamlit_app.py
```

Then open browser: http://localhost:8501

## Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/ask` | POST | Text RAG question |
| `/ask-image` | POST | Image search question |
| `/ask-sql` | POST | Natural language → SQL |
| `/memory` | GET | View conversation history |
| `/memory` | DELETE | Clear memory |

## Prerequisites

Before starting, make sure:
1. `python -m src.pipelines.ingest` has been run (text vectorstore)
2. `python -m src.retriever.image_search` has been run (image index)
3. `src/data/database/enterprise.db` exists (SQL database)
4. Ollama is running with Mistral: `ollama serve`

## Files Generated

- `CHAT-LOGS.json` — all conversation history
- `src/vectorstore/index.faiss` — text embeddings
- `src/vectorstore/image_index.faiss` — image embeddings