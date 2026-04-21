## Week Summary

| Day | Topic | Key Skill Learned |
|-----|-------|------------------|
| 1 | Architecture + Dataset | Transformer internals, data preparation |
| 2 | LoRA / QLoRA Training | Parameter-efficient fine-tuning |
| 3 | Quantisation | Model compression (8-bit, 4-bit, GGUF) |
| 4 | Inference Benchmarking | Speed/memory measurement, optimisation |
| 5 | API Deployment | Production LLM serving |


---

## Technical Achievements

### Fine-tuning (Day 2)
- Trained 1.1B param model with only 5-8M trainable params (< 1%)
- Used QLoRA: 4-bit base model + LoRA adapters
- Ran on Colab T4 GPU (free tier)
- Memory: ~1.2 GB VRAM vs ~4 GB for full fine-tuning

### Quantisation (Day 3)
- FP16 (2.2 GB) → INT8 (1.1 GB) → INT4 (550 MB) → GGUF q4_0 (~600 MB)
- 4× size reduction while preserving most quality
- GGUF: runs on CPU — no GPU needed

### Benchmarking (Day 4)
- Measured tokens/sec, VRAM, latency for each model version
- Base FP16: ~80 tok/s on GPU
- 4-bit quantised: ~55 tok/s (31% slower but 4× smaller)
- GGUF CPU: ~15-30 tok/s (no GPU needed!)

### API Deployment (Day 5)
- FastAPI server with POST /generate + POST /chat
- Multi-turn chat with session memory
- Streaming support (SSE)
- Request logging + unique IDs
- RAG context injection

---


## Key Concepts Mastered

### LoRA Math
```
Standard fine-tune: update W (d × d matrix) → d² parameters
LoRA:  W' = W + αΔW = W + α(A × B)
         A shape: (d, r), B shape: (r, d)
         Parameters: 2 × d × r (e.g., 2 × 2048 × 16 = 65,536)
         vs d² = 2048² = 4,194,304 (64× fewer parameters!)
```

### Quantisation Trade-offs
```
FP16 → INT8: Store each weight as integer in [-128, 127]
              Formula: int_val = round(float_val / scale) + zero_point
              Error: <1% perplexity increase

INT8 → INT4: 4-bit has only 16 distinct values!
              NF4 places these 16 values optimally for normal distributions
              Error: 1-3% perplexity increase
```