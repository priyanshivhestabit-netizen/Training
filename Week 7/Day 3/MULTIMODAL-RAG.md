## What is Image RAG?

Normal RAG works on text. Image RAG extends this to handle images — diagrams, charts,
scanned forms, engineering blueprints, damage photos, etc.

Instead of text chunks → text embeddings, we do:
**Images → OCR Text + BLIP Captions + CLIP Embeddings → FAISS → Query → Results**

---

## Pipeline Architecture

```
src/data/images/
      ↓
image_ingest.py
  ├── Tesseract OCR  → extracts printed text from image
  └── BLIP Caption   → generates description ("a pie chart showing...")
      ↓
clip_embedder.py
  └── CLIP embed_image() → converts image to 512-dim float32 vector
      ↓
image_search.py
  └── FAISS IndexFlatL2 → stores all image vectors
      ↓
User query (text)
  └── CLIP embed_text() → converts query to 512-dim vector
      ↓
FAISS search → nearest image vectors → return top-k results
```

---

## Components

### 1. `image_ingest.py` — Load & Describe Images

| Tool       | What it does                              |
|------------|-------------------------------------------|
| Tesseract  | OCR — reads printed/handwritten text      |
| BLIP       | Captioning — describes visual content     |

Output per image:
```json
{
  "path": "src/data/images/chart.png",
  "ocr_text": "Q1 Q2 Q3 Revenue...",
  "caption": "a bar chart showing quarterly revenue data",
  "text": "OCR: Q1 Q2 Q3... Caption: a bar chart...",
  "source": "chart.png"
}
```

### 2. `clip_embedder.py` — Generate Embeddings

| Function       | Input        | Output          |
|----------------|--------------|-----------------|
| embed_image()  | image path   | (512,) float32  |
| embed_text()   | query string | (1, 512) float32|

CLIP (Contrastive Language-Image Pretraining) is trained so that image vectors and
text vectors describing the same thing are close together in vector space.
This is why a text query like "bar chart" finds images of bar charts.

### 3. `image_search.py` — FAISS Index + Search

- **build_index(folder)** — loads all images, embeds them, stores in FAISS
- **save() / load()** — persist index to disk (so you don't rebuild every run)
- **search(query, k=3)** — text query → CLIP embedding → FAISS nearest neighbors

---

## How to Run

### First time (build index):
```bash
cd your_project_root
python -m src.retriever.image_search
```
This will:
1. Load images from `src/data/images/`
2. Run OCR + BLIP on each
3. Build FAISS index
4. Save to `src/vectorstore/image_index.faiss`

### After first time (index already saved):
Same command — it auto-detects the saved index and loads it.

---

## File Structure

```
src/
├── data/
│   └── images/          ← PUT YOUR IMAGES HERE (.png, .jpg, .jpeg)
├── embeddings/
│   └── clip_embedder.py
├── pipelines/
│   └── image_ingest.py
├── retriever/
│   └── image_search.py
└── vectorstore/
    ├── image_index.faiss  ← auto-generated
    └── image_meta.json    ← auto-generated
```

---

## Query Modes

| Mode             | Example                                         |
|------------------|-------------------------------------------------|
| Text → Image     | "show me diagrams of neural networks"           |
| Text → Image     | "find charts about quarterly revenue"           |
| Text → Image     | "engineering blueprint for pump system"         |

(Image → Image mode would require uploading a query image — not in scope for Day 3)

---

## Limitations

- BLIP captions are approximate; complex diagrams may get generic captions
- OCR quality depends on image resolution (use 300 DPI+ for best results)
- FAISS flat L2 is exact but slow at scale (use IVF index for 10k+ images)
- CLIP is 512-dim - good for general content, not fine-grained domain images

---

## Dependencies

```
transformers    # BLIP + CLIP models
torch           # model inference
Pillow          # image loading
pytesseract     # OCR
faiss-cpu       # vector search
numpy           # array ops
```