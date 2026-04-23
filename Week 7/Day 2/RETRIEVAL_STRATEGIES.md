## Overview

This project uses a two-stage hybrid retrieval pipeline: semantic search via FAISS followed by keyword re-scoring via `HybridRetriever`, with an optional reranking pass via `reranker.py`. Understanding why each stage exists, and where it can fail, is essential for tuning the system.

---

## Stage 1 — Dense Semantic Search (FAISS)

### What it does

Every document chunk is embedded into a 384-dimensional vector using `BAAI/bge-small-en` at ingestion time and stored in a FAISS `IndexFlatL2` index. At query time the same model embeds the question, and FAISS performs an exact L2 nearest-neighbour search over all stored vectors.

### Why L2 distance works here

All vectors are L2-normalised before storage (divided by their own magnitude so their length equals 1). On unit-length vectors, L2 distance and cosine similarity produce identical rankings — the relationship is `L2² = 2(1 − cos_sim)`. So the choice of L2 vs cosine is irrelevant once normalisation is applied, but L2 is faster in FAISS's flat index.

### Why `bge-small-en`

It is 33 million parameters, produces 384-dimensional vectors, and consistently ranks among the top small models on the MTEB retrieval benchmark. It is fast enough to run on CPU for typical document collections (under 100,000 chunks) without GPU hardware.

### Configuration

| Parameter | Value | Why |
|-----------|-------|-----|
| `chunk_size` | 800 chars | ~150–200 words; long enough for context, short enough for precise retrieval |
| `chunk_overlap` | 100 chars | 12.5% overlap prevents information loss at chunk boundaries |
| `k` in search | `k * 2` | Retrieves double the needed results for Stage 2 to rerank |

### Limitations

Pure semantic search can fail when the question contains rare keywords (product codes, proper nouns, version numbers) that the model was not trained to distinguish. Two chunks about completely different topics can score similarly if they share domain vocabulary.

---

## Stage 2 — Keyword Scoring (`HybridRetriever`)

### What it does

After Stage 1 returns `k*2` candidates, `HybridRetriever.keyword_score()` scores each chunk by counting how many query words appear in the chunk text. Results are sorted descending by this count and deduplicated before returning the top `k`.

### The scoring function

```python
def keyword_score(self, query, text):
    q_words = query.lower().split()
    t_words = text.lower().split()
    score = 0
    word_count = Counter(t_words)
    for word in q_words:
        score += word_count[word]
    return score
```

This is a simplified term-frequency (TF) score. `Counter` builds a frequency map of the chunk in O(n) time, and lookup per query word is O(1). The score increases once per occurrence of each query word in the chunk.

### What this catches that semantic search misses

If the question is "What is the error code 503 in our API?" and a chunk contains the literal string "503" several times, keyword scoring will promote it even if its semantic embedding is only moderately similar to the query. Exact string matching compensates for the semantic model's weakness on rare tokens.

### Known weaknesses

The current implementation splits on whitespace only — no stemming, no stop-word removal, no IDF weighting. This means:
- "running" and "run" score as different words
- Common words like "the", "is", "a" contribute to the score equally as content words
- A chunk that simply repeats the question's stop words scores higher than a more relevant chunk with slightly different vocabulary

For a production upgrade, replace this with BM25 using the `rank_bm25` library.

### Deduplication

```python
seen = set()
for item, score in scored:
    if item["text"] not in seen:
        seen.add(item["text"])
        final.append(item)
```

FAISS can return the same chunk twice if it appears in multiple storage calls or if approximate indexing is later introduced. The `seen` set uses the full chunk text as the key. This is not ideal — for large chunks, hashing the text would be more memory-efficient. A better key would be `chunk_id` from metadata.

---

## Stage 3 — Reranker (`reranker.py`)

### Current state — redundant

The reranker uses `bge-small-en` cosine similarity, which is the same model and metric used for FAISS retrieval in Stage 1. Computing it again produces the same ranking as Stage 1's semantic order, before Stage 2 keyword re-scoring. In practice this means the reranker partially undoes the hybrid retrieval by re-imposing the pure semantic order.

**This is a bug, not a feature.** It should be fixed or removed.

### How to fix it — use a cross-encoder

A cross-encoder jointly encodes the query and each document together as a single input, producing a relevance score that is substantially more accurate than bi-encoder cosine similarity.

```python
from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query, results):
    pairs = [[query, item["text"]] for item in results]
    scores = cross_encoder.predict(pairs)
    scored = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
    return [item for item, _ in scored]
```

`ms-marco-MiniLM-L-6-v2` is trained on the MS MARCO passage retrieval dataset and produces relevance scores on a continuous scale. It is slower than bi-encoder search (because each query-document pair is processed together) but should only be used on the small reranking candidate set (typically 10–20 chunks), not the full index.

### When to keep the reranker vs remove it

Keep it if you replace it with a cross-encoder. Remove it if you are working with limited compute, since the current implementation adds latency with no accuracy benefit.

---

## Retrieval Flow Diagram

```
User question
      │
      ▼
embed_texts([question])          ← bge-small-en, 384-dim vector
      │
      ▼
FAISSStore.search(q_emb, k*2)   ← L2 nearest-neighbour over all chunks
      │
      ▼
HybridRetriever.keyword_score() ← TF scoring, sort, deduplicate → top k
      │
      ▼
rerank(query, results)           ← currently redundant; should be cross-encoder
      │
      ▼
top k chunks passed to generate_answer()
```

---

## Tuning Guide

### If answers are too generic or miss specifics

Lower `chunk_size` to 400–500 characters. Smaller chunks are more targeted. Increase `k` to 5 or 7 so more evidence is available.

### If answers are incoherent or miss context

Raise `chunk_size` to 1,000–1,200. Increase `chunk_overlap` to 150–200. The model needs more surrounding context per chunk.

### If keyword-heavy queries fail

Implement BM25 alongside the current keyword scorer and blend scores: `final_score = 0.6 * semantic_score + 0.4 * bm25_score`. This is the standard hybrid retrieval formula.

### If latency is too high

Replace `IndexFlatL2` (exact) with `IndexIVFFlat` (approximate). This trades a small amount of recall for significantly faster search on large indexes (over 100,000 chunks). You will need to train the IVF index on a sample of your embeddings before use.

---

## Files Involved

| File | Role |
|------|------|
| `src/embeddings/embedder.py` | Produces bge-small-en text embeddings |
| `src/vectorstore/faiss_store.py` | Stores and searches embeddings |
| `src/retriever/hybrid_retriever.py` | Combines semantic + keyword scoring |
| `src/retriever/reranker.py` | Optional reranking pass (currently redundant) |
| `src/pipelines/ingest.py` | Chunks documents and builds the FAISS index |