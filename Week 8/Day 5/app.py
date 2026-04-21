import uuid
import time
import logging
import asyncio
from datetime import datetime
from collections import defaultdict
from typing import Optional, List, Dict
import uvicorn

# FastAPI
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

#modules
from config import MODEL_CONFIG, GENERATION_DEFAULTS,SERVER_CONFIG, LIMITS
from model_loader import model_loader

# Logging setup 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("llm_api")

# FastAPI App
app = FastAPI(
    title="Week 8 LLM API",
    description=(
        "Local LLM inference server — Fine-tuned TinyLlama\n"
    ),
    version="1.0.0",
)

chat_sessions: Dict[str, List[Dict[str, str]]] = defaultdict(list)

request_log: List[Dict] = []

rate_limit_store: Dict[str, List[float]] = defaultdict(list)


class GenerateRequest(BaseModel):
    instruction: str = Field(..., description="The instruction/question for the model")
    input: Optional[str] = Field("", description="Optional additional input/context")
    max_new_tokens: Optional[int] = Field(
        GENERATION_DEFAULTS["max_new_tokens"], ge=1, le=2048
    )
    temperature: Optional[float] = Field(
        GENERATION_DEFAULTS["temperature"], ge=0.0, le=2.0
    )
    top_p: Optional[float] = Field(GENERATION_DEFAULTS["top_p"], ge=0.0, le=1.0)
    top_k: Optional[int] = Field(GENERATION_DEFAULTS["top_k"], ge=0, le=100)
    repetition_penalty: Optional[float] = Field(
        GENERATION_DEFAULTS["repetition_penalty"], ge=1.0, le=2.0
    )
    stream: Optional[bool] = Field(False, description="Enable streaming response")
    context: Optional[str] = Field(
        None, description="RAG context"
    )

class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's new message")
    session_id: Optional[str] = Field(
        None, description="Session ID for conversation continuity. Auto-generated if not provided."
    )
    system_prompt: Optional[str] = Field(None, description="System prompt")
    max_new_tokens: Optional[int] = Field(GENERATION_DEFAULTS["max_new_tokens"], ge=1, le=2048)
    temperature: Optional[float] = Field(GENERATION_DEFAULTS["temperature"], ge=0.0, le=2.0)
    top_p: Optional[float] = Field(GENERATION_DEFAULTS["top_p"], ge=0.0, le=1.0)
    top_k: Optional[int] = Field(GENERATION_DEFAULTS["top_k"], ge=0, le=100)
    stream: Optional[bool] = Field(False)
    context: Optional[str] = Field(None, description="RAG context for this turn")
    clear_history: Optional[bool] = Field(False, description="Clear conversation history")

class GenerateResponse(BaseModel):
    request_id: str
    response: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_sec: float
    timestamp: str

class ChatResponse(BaseModel):
    request_id: str
    session_id: str
    response: str
    model: str
    history_length: int
    latency_sec: float
    timestamp: str

def generate_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"

def log_request(request_id: str, endpoint: str, request_data: dict, response_data: dict):
    log_entry = {
        "request_id": request_id,
        "endpoint": endpoint,
        "timestamp": datetime.now().isoformat(),
        "request": {k: str(v)[:100] for k, v in request_data.items()},
        "response_preview": str(response_data.get("response", ""))[:200],
        "latency_sec": response_data.get("latency_sec"),
    }
    request_log.append(log_entry)
    # Keep only last 1000 entries in memory
    if len(request_log) > 1000:
        request_log.pop(0)
    logger.info(
        f"[{request_id}] {endpoint} | "
        f"latency={response_data.get('latency_sec', '?')}s"
    )

def check_rate_limit(client_ip: str):
    now = time.time()
    window = 60  # 1 minute
    max_requests = LIMITS["rate_limit_per_minute"]

    # Clean old entries
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip] if now - t < window
    ]

    if len(rate_limit_store[client_ip]) >= max_requests:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {max_requests} requests/minute"
        )
    rate_limit_store[client_ip].append(now)

def build_alpaca_prompt(
    instruction: str,
    input_text: str = "",
    context: Optional[str] = None,
) -> str:
    if context:
        input_text = f"{context}\n{input_text}".strip()

    if input_text and input_text.strip():
        return f"""### Instruction:
{instruction}

### Input:
{input_text}

### Response:
"""
    else:
        return f"""### Instruction:
{instruction}

### Response:
"""

def build_chat_prompt(
    history: List[Dict[str, str]],
    system_prompt: Optional[str] = None,
    context: Optional[str] = None,
) -> str:
    prompt_parts = []
    
    if system_prompt:
        prompt_parts.append(f"### System:\n{system_prompt}\n")
    
    for msg in history:
        if msg["role"] == "user":
            prompt_parts.append(f"### Instruction:\n{msg['content']}\n")
        else:  # assistant
            prompt_parts.append(f"### Response:\n{msg['content']}\n")
    
    if context:
        prompt_parts.append(f"### Context:\n{context}\n")
    
    prompt_parts.append("### Response:\n")
    
    return "\n".join(prompt_parts)


def estimate_token_count(text: str) -> int:
    """Quick token estimate (words × 1.3)"""
    return int(len(text.split()) * 1.3)


@app.on_event("startup")
async def startup_event():
    logger.info("Week 8 LLM API Server starting...")
    logger.info(f"Model mode: {MODEL_CONFIG['mode']}")

    loop = asyncio.get_event_loop()
    success = await loop.run_in_executor(None, model_loader.load, MODEL_CONFIG)

    if success:
        info = model_loader.get_model_info()
        logger.info(f"Model ready in {info['load_time_sec']}s")
        logger.info(f"VRAM used: {info['vram_used_gb']} GB")
    else:
        logger.error("Model failed to load! Check configuration.")


# ------ ROUTES -----

@app.get("/health")
async def health_check():
    model_info = model_loader.get_model_info()
    return {
        "status": "healthy" if model_info["loaded"] else "degraded",
        "model_loaded": model_info["loaded"],
        "timestamp": datetime.now().isoformat(),
        "server": "Week 8 LLM API v1.0",
    }

@app.get("/model")
async def model_info():
    info = model_loader.get_model_info()
    info["config"] = {
        "base_model": MODEL_CONFIG["base_model"],
        "mode": MODEL_CONFIG["mode"],
        "quantization": MODEL_CONFIG["quantization"],
    }
    info["defaults"] = GENERATION_DEFAULTS
    return info

@app.get("/logs")
async def get_logs(limit: int = 50):
    return {
        "total_requests": len(request_log),
        "recent": request_log[-limit:],
    }

@app.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    if session_id in chat_sessions:
        chat_sessions.pop(session_id)
        return {"message": f"Session {session_id} cleared"}
    raise HTTPException(status_code=404, detail="Session not found")


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest, http_request: Request):
    request_id = generate_request_id()

    # Rate limit check
    client_ip = http_request.client.host if http_request.client else "unknown"
    check_rate_limit(client_ip)

    # Model check
    if not model_loader.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded. Try again in a moment.")

    # Validate prompt length
    if len(request.instruction) > LIMITS["max_prompt_length"]:
        raise HTTPException(
            status_code=400,
            detail=f"Instruction too long. Max {LIMITS['max_prompt_length']} chars."
        )

    # Build prompt
    prompt = build_alpaca_prompt(
        instruction=request.instruction,
        input_text=request.input or "",
        context=request.context,
    )

    if request.stream:
        async def stream_generator():
            try:
                full_response = []
                for token in model_loader.generate_stream(
                    prompt,
                    max_new_tokens=request.max_new_tokens,
                    temperature=request.temperature,
                    top_p=request.top_p,
                ):
                    full_response.append(token)
                    yield f"data: {token}\n\n"
                
                complete = "".join(full_response)
                if "###" in complete:
                    complete = complete.split("###")[0].strip()
                
                yield f"data: [DONE]\n\n"
            except Exception as e:
                yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",
            headers={"X-Request-ID": request_id},
        )

    start = time.perf_counter()
    try:
        loop = asyncio.get_event_loop()
        response_text = await loop.run_in_executor(
            None,
            lambda: model_loader.generate(
                prompt,
                max_new_tokens=request.max_new_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                top_k=request.top_k,
                repetition_penalty=request.repetition_penalty,
            ),
        )
        
        response_text = response_text.strip()
        if "###" in response_text:
            response_text = response_text.split("###")[0].strip()
            
    except Exception as e:
        logger.error(f"[{request_id}] Generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

    latency = round(time.perf_counter() - start, 3)
    prompt_tokens = estimate_token_count(prompt)
    completion_tokens = estimate_token_count(response_text)

    response_data = {
        "request_id": request_id,
        "response": response_text,
        "model": f"{MODEL_CONFIG['base_model']} ({MODEL_CONFIG['mode']})",
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "latency_sec": latency,
        "timestamp": datetime.now().isoformat(),
    }

    log_request(request_id, "/generate", request.dict(), response_data)
    return response_data

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request):
    request_id = generate_request_id()

    # Rate limit
    client_ip = http_request.client.host if http_request.client else "unknown"
    check_rate_limit(client_ip)

    if not model_loader.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Session management
    session_id = request.session_id or f"sess_{uuid.uuid4().hex[:8]}"

    if request.clear_history:
        chat_sessions[session_id] = []
        logger.info(f"[{request_id}] Session {session_id} history cleared")

    # Get/init session history
    history = chat_sessions[session_id]

    # Add user message to history
    history.append({"role": "user", "content": request.message})

    # Build prompt with FULL history
    prompt = build_chat_prompt(history, request.system_prompt, request.context)

    # Streaming chat
    if request.stream:
        collected_response = []

        async def chat_stream():
            try:
                for token in model_loader.generate_stream(
                    prompt,
                    max_new_tokens=request.max_new_tokens,
                    temperature=request.temperature,
                    top_p=request.top_p,
                ):
                    collected_response.append(token)
                    yield f"data: {token}\n\n"

                # Save complete response to history
                full_response = "".join(collected_response).strip()
                # Clean response
                if "###" in full_response:
                    full_response = full_response.split("###")[0].strip()
                history.append({"role": "assistant", "content": full_response})
                yield f"data: [DONE]\n\n"
            except Exception as e:
                yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(
            chat_stream(),
            media_type="text/event-stream",
            headers={
                "X-Request-ID": request_id,
                "X-Session-ID": session_id,
            },
        )

    # Standard chat response
    start = time.perf_counter()
    try:
        loop = asyncio.get_event_loop()
        response_text = await loop.run_in_executor(
            None,
            lambda: model_loader.generate(
                prompt,
                max_new_tokens=request.max_new_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                top_k=request.top_k,
            ),
        )
        
        # Clean response
        response_text = response_text.strip()
        if "###" in response_text:
            response_text = response_text.split("###")[0].strip()
            
    except Exception as e:
        history.pop()
        logger.error(f"[{request_id}] Chat generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

    latency = round(time.perf_counter() - start, 3)

    # Add assistant response to history
    history.append({"role": "assistant", "content": response_text})

    # Trim history to max length
    if len(history) > LIMITS["max_chat_history"] * 2:
        history = history[-(LIMITS["max_chat_history"] * 2):]
        chat_sessions[session_id] = history

    response_data = {
        "request_id": request_id,
        "session_id": session_id,
        "response": response_text,
        "model": f"{MODEL_CONFIG['base_model']} ({MODEL_CONFIG['mode']})",
        "history_length": len(history),
        "latency_sec": latency,
        "timestamp": datetime.now().isoformat(),
    }

    log_request(request_id, "/chat", {"session_id": session_id, "message": request.message}, response_data)
    return response_data


@app.get("/chat/{session_id}/history")
async def get_chat_history(session_id: str):
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": session_id,
        "history": chat_sessions[session_id],
        "turn_count": len(chat_sessions[session_id]) // 2,
    }


if __name__ == "__main__":
    print("Starting Week 8 LLM API Server")
    print(f"URL: http://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}")
    print(f"Docs: http://localhost:{SERVER_CONFIG['port']}/docs")
    print(f"Model mode: {MODEL_CONFIG['mode']}")

    uvicorn.run(
        "app:app",
        host=SERVER_CONFIG["host"],
        port=SERVER_CONFIG["port"],
        reload=False,
        log_level=SERVER_CONFIG["log_level"],
    )