import faiss
import numpy as np
import json
import os

from src.embeddings.clip_embedder import embed_image, embed_text
from src.pipelines.image_ingest import load_images, extract_text, generate_caption

INDEX_PATH = "src/vectorstore/image_index.faiss"
META_PATH  = "src/vectorstore/image_meta.json"


class ImageSearch:
    def __init__(self):
        self.index = None
        self.data = []

    def build_index(self, folder):
        print(f"Building image index from: {folder}")
        images = load_images(folder)

        if not images:
            print("No images found in folder!")
            return

        embeddings = []
        for img in images:
            emb = embed_image(img["path"])
            embeddings.append(emb.reshape(1, -1))
            self.data.append({
                "path":     img["path"],
                "text":     img["text"],
                "ocr_text": img["ocr_text"],
                "caption":  img["caption"],
                "source":   img["source"]
            })

        embeddings = np.vstack(embeddings).astype("float32")
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        print(f"Image index built with {len(self.data)} images")
        self.save()

    def save(self):
        os.makedirs("src/vectorstore", exist_ok=True)
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "w") as f:
            json.dump(self.data, f, indent=2)
        print(f"Image index saved → {INDEX_PATH}")

    @classmethod
    def load(cls):
        obj = cls()
        obj.index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "r") as f:
            obj.data = json.load(f)
        print(f"Image index loaded — {len(obj.data)} images")
        return obj

    def search_by_text(self, query, k=3):
        q_emb = embed_text(query).reshape(1, -1).astype("float32")
        D, I = self.index.search(q_emb, k)
        return [self.data[i] for i in I[0] if i < len(self.data)]

    def search_by_image(self, image_path, k=3):
        q_emb = embed_image(image_path).reshape(1, -1).astype("float32")
        D, I = self.index.search(q_emb, k)

        results = []
        for i in I[0]:
            if i < len(self.data):
                if os.path.abspath(self.data[i]["path"]) != os.path.abspath(image_path):
                    results.append(self.data[i])
        return results[:k]

   
    def image_to_text(self, image_path):
        print(f"Analyzing image: {image_path}")

        ocr     = extract_text(image_path)
        caption = generate_caption(image_path)

        similar = self.search_by_image(image_path, k=2)

        answer  = "=== IMAGE ANALYSIS ===\n"
        answer += f"Caption  : {caption}\n"
        answer += f"OCR Text : {ocr if ocr else 'No text found in image'}\n"

        if similar:
            answer += "\n=== RELATED IMAGES IN INDEX ===\n"
            for i, s in enumerate(similar, 1):
                answer += f"  Related {i}: {s['source']}\n"
                answer += f"  Caption  : {s['caption']}\n"
                answer += f"  OCR      : {s['ocr_text'][:100] if s['ocr_text'] else 'None'}\n"

        return answer


def run():
    image_folder = "src/data/images"

    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        print("Loading existing image index...")
        engine = ImageSearch.load()
    else:
        print("No index found. Building from images folder...")
        engine = ImageSearch()
        engine.build_index(image_folder)

    if engine.index is None:
        print("Could not build index. Add images to src/data/images/")
        return

    print("\n" + "="*50)
    print("IMAGE SEARCH — 3 MODES AVAILABLE")
    print("="*50)
    print("  1 → Text to Image   (type a query)")
    print("  2 → Image to Image  (give image path)")
    print("  3 → Image to Text   (analyze an image)")
    print("  exit → Quit")
    print("="*50 + "\n")

    while True:
        mode = input("Choose mode (1/2/3/exit): ").strip()

        if mode == "exit":
            break

        elif mode == "1":
            query = input("  Enter text query: ").strip()
            results = engine.search_by_text(query, k=3)
            print(f"\n  Top {len(results)} results:")
            for i, r in enumerate(results, 1):
                print(f"    [{i}] {r['source']}")
                print(f"        Caption : {r['caption']}")
                print(f"        OCR     : {r['ocr_text'][:100] if r['ocr_text'] else 'None'}")
            print()

        elif mode == "2":
            path = input("  Enter image path (e.g. src/data/images/bar_chart.jpg): ").strip()
            if not os.path.exists(path):
                print(f"  File not found: {path}\n")
                continue
            results = engine.search_by_image(path, k=3)
            if not results:
                print("  No similar images found (only 1 image in index — add more!)\n")
            else:
                print(f"\n  Similar images:")
                for i, r in enumerate(results, 1):
                    print(f"    [{i}] {r['source']}")
                    print(f"        Caption : {r['caption']}")
            print()

        elif mode == "3":
            path = input("  Enter image path to analyze: ").strip()
            if not os.path.exists(path):
                print(f"  File not found: {path}\n")
                continue
            answer = engine.image_to_text(path)
            print(f"\n{answer}")

        else:
            print("  Invalid choice. Enter 1, 2, 3, or exit.\n")


if __name__ == "__main__":
    run()