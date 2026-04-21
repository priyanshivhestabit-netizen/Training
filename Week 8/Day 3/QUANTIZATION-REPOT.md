# QUANTISATION REPORT

## What is Quantisation?

Quantisation = reducing the precision of model weights to save memory.

Neural network weights are originally stored as FP32 (32-bit floating point numbers). We reduce them:

```
FP32 (4 bytes) → FP16 (2 bytes) → INT8 (1 byte) → INT4 (0.5 bytes)
```

Like compressing an image: TIFF → PNG → JPEG (more compression, slightly less quality)

## Formats Explained

### FP16 (Half Precision)
- **Size**: ~2.2 GB for TinyLlama 1.1B (Disk: ~{{fp16_size:.1f}} GB)
- **Quality**: Identical to FP32 (negligible loss)
- **Use**: GPU inference, training

### INT8 (8-bit Integer)
- **Size**: **In-memory: ~1.24 GB (~2x smaller in VRAM)**; **Disk: ~1.24 GB** (Weights saved mostly as FP16 with `quantization_config`)
- **Method**: bitsandbytes LLM.int8()
- **How**: Weights scaled to integer range [-128, 127]
- **Trick**: Outlier weights (large values) kept in FP16 → preserves accuracy
- **Quality**: ~0.5-1% perplexity increase (practically identical)
- **Use**: GPU with less VRAM

### INT4 (4-bit, NF4)
- **Size**: **In-memory: ~0.77 GB (~4x smaller in VRAM)**; **Disk: ~0.77 GB** (Weights saved mostly as FP16 with `quantization_config`)
- **Method**: bitsandbytes NF4 with double quantisation
- **NF4**: Normal Float 4 — designed for normally-distributed NN weights
- **Double quant**: Quantise the quantisation constants too (saves extra 50MB)
- **Quality**: ~1-3% perplexity increase (good for most tasks)
- **Use**: GPU with minimal VRAM (T4 easily handles it)

### GGUF ({{QUANT_TYPE}})
- **Size**: **~0.64 GB**
- **Tool**: llama.cpp
- **Key advantage**: Runs on CPU — no GPU needed!
- **Quality**: Similar to INT4
- **Use**: Laptop, edge deployment, no-GPU environments

## Quantization Results Table

| Format        | Size (Disk, GB)        | Speed (Tokens/sec)  | Quality                  |
|---------------|------------------------|---------------------|--------------------------|
| FP16 (Baseline) | 2.20 (Model only)    | 12.7                | Baseline                 |
| INT8          | 1.24 (FP16+Config)     | 4.9                 | Good (Minor drop)        |
| INT4 (NF4)    | 0.77 (FP16+Config)     | 18.2                | Acceptable (Noticeable drop) |
| GGUF (q4_0)   | 0.64 (CPU format)      | 4.6                 | Good                     |

## How to Run

```bash
cd Week8/Day3
pip install transformers peft bitsandbytes -q
python scripts/quantize.py
```

## Folder Structure After Running

```
quantized/
├── merged_fp16/          <- Base + adapter merged
│   ├── model.safetensors
│   └── config.json
├── model-int8/           ← 8-bit quantized (contains FP16 weights + config)
├── model-int4/           ← 4-bit quantized (contains FP16 weights + config)
├── model.gguf            ← GGUF format (CPU-ready, truly quantized on disk)
└── quantisation_results.json
```

## Verify GGUF Works

```bash
# Install llama.cpp Python bindings
pip install llama-cpp-python

# Test inference
python -c "
from llama_cpp import Llama
llm = Llama(model_path='quantized/model.gguf', n_ctx=512)
out = llm('### Instruction:\nWhat is interest?\n\n### Response:\n', max_tokens=100)
print(out['choices'][0]['text'])
"
```