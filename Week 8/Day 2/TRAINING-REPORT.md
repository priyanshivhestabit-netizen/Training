## Model & Method

| Setting | Value |
|---------|-------|
| Base Model | TinyLlama/TinyLlama-1.1B-Chat-v1.0 |
| Method | QLoRA (4-bit quantization + LoRA) |
| LoRA Rank (r) | 16 |
| LoRA Alpha | 32 |
| Dropout | 0.05 |
| Target Modules | q_proj, k_proj, v_proj, o_proj |

## Training Config

| Hyperparameter | Value | Reason |
|----------------|-------|--------|
| Learning Rate | 2e-4 | Standard for LoRA (higher than full FT) |
| Batch Size | 4 | Per device |
| Gradient Accum | 4 | Effective batch = 16 |
| Epochs | 3 | Enough for 1200 samples |
| Scheduler | Cosine | Smooth LR decay |
| Optimizer | paged_adamw_8bit | 8-bit saves VRAM |

## Parameter Efficiency

| Metric | Value |
|--------|-------|
| Total Parameters | 1,102,301,184 |
| Trainable Parameters | 2,252,800 |
| Trainable % | 0.2044 |


## Why These Settings Work

**r=16**: This rank means LoRA adds matrices of shape [hidden_dim, 16] × [16, hidden_dim]. Higher rank = more capacity but more parameters. For domain adaptation, r=16 is a sweet spot.

**alpha=32**: alpha/r = 2.0 is the scaling factor. Keeps updates at reasonable magnitude so they don't overwrite the original knowledge entirely.

**4-bit loading**: Without quantization, 1.1B params × 4 bytes = 4.4GB VRAM just for weights. With 4-bit: ~550MB. This is why we can train on Colab's T4 GPU.

**Gradient checkpointing**: Instead of storing all intermediate activations during forward pass (needed for backward pass), recompute them on demand. Uses 30-40% less VRAM at cost of ~20% slower training.

## Expected Training Metrics

| Epoch | Train Loss | Val Loss |
|-------|-----------|----------|
| 1 | 2.508500 | 1.954611 |
| 2 | 1.834200 | 1.621253 |
| 3 | 1.412100 | 1.458231 |


## Adapter Files

```
adapters/
├── adapter_config.json      — LoRA configuration
├── adapter_model.safetensors — Trained LoRA weights
└── tokenizer files          — Tokenizer config
```

## How to Load for Inference

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
model = PeftModel.from_pretrained(base_model, "adapters/")
tokenizer = AutoTokenizer.from_pretrained("adapters/")
```