# Dataset Analysis

## Dataset Overview

This dataset is created for instruction fine-tuning of a Large Language Model (LLM) in the **Finance domain**.

It follows the standard instruction tuning format:

​```json
{"instruction": "...", "input": "...", "output": "..."}
​```

## Dataset Composition

The dataset contains three types of tasks:

1. **Question Answering (QA)** — Concept-based financial questions
   - "What is inflation?"
   - "What is equity?"

2. **Reasoning Tasks** — Numerical and logical financial problems with step-by-step explanations
   - ROI calculation
   - Real growth calculation
   - Stock percentage gain

3. **Information Extraction** — Extract structured data from text
   - Company revenue extraction
   - Profit & year identification

## Dataset Size

| Dataset    | Samples |
|------------|---------|
| Train      | ~1000   |
| Validation | ~200    |

## Token Length Analysis

**Train Dataset**
- Min tokens: 15
- Max tokens: 39
- Average tokens: 24.52

**Validation Dataset**
- Min tokens: 22
- Max tokens: 38
- Average tokens: 28.3

**3. Clean Dataset**
- No empty outputs
- No malformed JSON
- No extreme outliers

## Train vs Validation Strategy

| Aspect    | Train                    | Validation                    |
|-----------|--------------------------|-------------------------------|
| Purpose   | Learning                 | Evaluation                    |
| Style     | Step-by-step reasoning   | Explanation-based reasoning   |
| Data      | Randomized               | Different randomized samples  |

> **Key Principle:** Same format, different data to avoid memorization.