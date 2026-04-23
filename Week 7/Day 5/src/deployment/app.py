import os
import sys
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.insert(0, os.getcwd())

import ollama
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.memory.memory_store import memory
from src.evaluation.rag_eval import evaluate
from src.pipelines.sql_pipeline import run_sql_qa
from src.retriever.image_search import  ImageSearch,    INDEX_PATH,META_PATH
from src.vectorstore.faiss_store import FAISSStore
from src.retriever.hybrid_retriever import  HybridRetriever
from src.prompts import get_answer_prompt, get_refine_prompt

app = FastAPI(title = "Advanced RAG")

# Load text vector store once at startup
text_store = None
text_retriever = None

if os.path.exists("src/vectorstore/index.faiss"):
    text_store = FAISSStore.load()
    text_retriever = HybridRetriever(text_store)
    print("Text vectore store loaded")

else:
    print(" WARNING : No text vectorstore found. Run ingest.py first")

# Load image index once at startup
image_engine = None

if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
    image_engine = ImageSearch.load()
    print("Image index loaded")
else:
    print("WARNING : No image index found. Run image_search first")

# request-response models

class AskRequest(BaseModel):
    question: str
    k: int = 3

class ImageAskRequest(BaseModel):
    query: str
    k: int = 3

class ImageToImageRequest(BaseModel):
    image_path: str
    k: int = 3
 
class ImageToTextRequest(BaseModel):
    image_path: str

class SqlAskRequest(BaseModel):
    question: str

# helper: generate answer using Mistral + context
def generate_answer(question, context_chunks, conversation_history=""):
    context_text = "\n\n".join(
        c.get("text","")[:400] if isinstance(c,dict) else str(c)[:400]
        for c in context_chunks
    )

    prompt = get_answer_prompt(question, context_text, conversation_history)
    response = ollama.chat(model="mistral", messages=[{
        "role":"user",
        "content": prompt
    }])
    return response["message"]["content"].strip()

def refine_answer(question, answer,eval_result):
    if not eval_result["is_hallucinated"] and eval_result["confidence_pct"]>=40:
        return answer
    prompt = get_refine_prompt(question,answer)
    response = ollama.chat(model = "mistral", messages =[{
        "role":"user",
        "content":prompt
    }])
    return response["message"]["content"].strip()

# api endpoints

@app.post("/ask")
def ask(req: AskRequest):
    if not text_retriever:
        raise HTTPException(status_code=503, detail="text  vectorestore not loaded")
    
    history = memory.get_context()
    chunks = text_retriever.query(req.question,k=req.k)
    answer = generate_answer(req.question,chunks,history)
    eval_res = evaluate(answer,chunks)
    final = refine_answer(req.question, answer, eval_res)

    memory.add("user",req.question,"/ask")
    memory.add("assistant",final,"/ask")

    return{
        "question": req.question,
        "answer": final,
        "sources": [c.get("source","unknown") for c in chunks],
        "evaluation": eval_res,
        "chunks_used":len(chunks)
    }

@app.post("/ask-image")
def ask_image(req: ImageAskRequest):
    if not image_engine:
        raise HTTPException(status_code=503, detail="Image index not loaded.")
 
    results  = image_engine.search_by_text(req.query, k=req.k)
    if not results:
        return {"query": req.query, "results": [], "answer": "No relevant images found."}
 
    context  = [{"text": r["text"]} for r in results]
    answer   = generate_answer(req.query, context, memory.get_context())
    eval_res = evaluate(answer, context)
 
    memory.add("user",req.query, "/ask-image")
    memory.add("assistant", answer,"/ask-image")
 
    return {
        "query":req.query,
        "answer":answer,
        "images":[{"source": r["source"], "caption": r["caption"]} for r in results],
        "evaluation": eval_res
    }
 
@app.post("/image-to-image")
def image_to_image(req: ImageToImageRequest):
    if not image_engine:
        raise HTTPException(status_code=503, detail="Image index not loaded.")
 
    if not os.path.exists(req.image_path):
        raise HTTPException(status_code=404, detail=f"Image not found: {req.image_path}")
 
    similar = image_engine.search_by_image(req.image_path, k=req.k)
 
    memory.add("user",      f"[Image→Image] uploaded image", "/ask-image")
    memory.add("assistant", f"Found {len(similar)} similar images", "/ask-image")
 
    return {
        "query_image":    req.image_path,
        "similar_images": [
            {
                "source":   r["source"],
                "caption":  r["caption"],
                "ocr_text": r.get("ocr_text", "")
            }
            for r in similar
        ]
    }

@app.post("/image-to-text")
def image_to_text(req: ImageToTextRequest):
    if not image_engine:
        raise HTTPException(status_code=503, detail="Image index not loaded.")
 
    if not os.path.exists(req.image_path):
        raise HTTPException(status_code=404, detail=f"Image not found: {req.image_path}")
 
    from src.pipelines.image_ingest import extract_text, generate_caption
 
    ocr_text = extract_text(req.image_path)
    caption  = generate_caption(req.image_path)
    related  = image_engine.search_by_image(req.image_path, k=2)
 
    # Build context for LLM summary
    context_text = f"Image caption: {caption}\nOCR text: {ocr_text if ocr_text else 'No text found'}"
    if related:
        context_text += "\n\nRelated images:\n"
        for r in related:
            context_text += f"- {r['source']}: {r['caption']} | {r.get('ocr_text','')[:100]}\n"
 
    summary_prompt = f"""Analyze this image information and provide a clear summary:
 
{context_text}
 
Write 2-3 sentences describing what this image contains and what information it conveys.
"""
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": summary_prompt}])
    summary  = response["message"]["content"].strip()
 
    memory.add("user",      "[Image→Text] uploaded image for analysis", "/ask-image")
    memory.add("assistant", summary, "/ask-image")
 
    return {
        "image_path":     req.image_path,
        "caption":        caption,
        "ocr_text":       ocr_text,
        "summary":        summary,
        "related_images": [
            {"source": r["source"], "caption": r["caption"]}
            for r in related
        ]
    }

@app.post("/ask-sql")
def ask_sql(req: SqlAskRequest):
    result = run_sql_qa(req.question)
    memory.add("user",req.question,"/ask-sql")
    memory.add("assistant", result["summary"], "/ask-sql")
    return {
        "question": req.question,
        "sql": result["sql"],
        "table": result.get("table", ""),
        "summary":result["summary"],
        "error": result.get("error")
    }
 
@app.get("/memory")
def get_memory():
    return {"history": memory.history}
 
@app.delete("/memory")
def clear_memory():
    memory.clear()
    return {"message": "Memory cleared."}
 
@app.get("/")
def root():
    return {
        "status": "running", 
        "endpoints": ["/ask", "/ask-image", "/ask-sql", "/memory"]
        }
 