# BENCHMARK REPORT — Week 8, Day 4

## Inference Optimization Concepts

### KV Cache
The most important optimization for autoregressive LLMs:
- Every token generation needs attention over ALL previous tokens
- Without cache: recompute key/value for all previous tokens each step → O(n²)
- With cache: store computed K/V, only compute new token → O(n)
- Result: 2-5x faster inference for long outputs

### Streaming
- Normal: wait for full generation (30+ seconds) before displaying
- Streaming: display each token as generated (like ChatGPT)
- Implementation: `TextStreamer` from transformers
- User experience: feels instant even for long outputs

### Batch Inference
- Process N prompts simultaneously on GPU (parallel)
- Trade-off: higher latency per prompt, but N× higher throughput
- Good for: offline eval, batch processing, API serving with many users

### vLLM (Production)
- Advanced serving framework for LLMs
- Continuous batching: don't wait for slowest request in batch
- PagedAttention: efficient KV cache memory management
- Can serve 10-100× more requests than naive serving

## Benchmark Results

| Model | avg tok/s | Latency | VRAM |
|-------|-----------|---------|------|
| Base FP16 | ~80 | ~1.5s | ~2GB |
| Fine-tuned (4bit) | ~70 | ~1.8s | ~1.2GB |
| Quantised 4-bit | ~55 | ~2.2s | ~0.6GB |
| GGUF (CPU) | ~15-30 | ~5-10s | 0 |

## How to Run

```bash
cd Week8/Day4
pip install transformers peft bitsandbytes -q
python test_inference.ipynb
```

For GGUF CPU test:
```bash
pip install llama-cpp-python --prefer-binary
python test_inference.ipynb  # Runs GGUF test at the end
```

## Verify Results

After running, check:
```python
import pandas as pd
df = pd.read_csv('benchmarks/results.csv')
print(df.groupby('model')['tokens_per_sec'].mean())
```

## Connection to Week 7

Week 7: Ollama served Mistral → you made API calls to it
Week 8 Day 4: You see exactly how that works:
- Ollama = llama.cpp + GGUF + HTTP server
- You measured that GGUF gives ~15-30 tok/s on CPU
- That's exactly what your Week 7 Ollama was doing!
Week 8 Day 5: You'll build your OWN version of what Ollama does.