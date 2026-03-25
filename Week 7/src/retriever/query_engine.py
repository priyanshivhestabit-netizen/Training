from src.pipelines.ingest import main as ingest_main, embed_texts


class Retriever:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def query(self, question, k=3):
        q_emb = embed_texts([question])
        results = self.vectorstore.search(q_emb, k)

        formatted = []
        for r in results:
            formatted.append({
                "source": r["source"],
                "chunk": r["chunk"],
                "text": r["text"][:300]
            })

        return formatted


def run():
    print("Building vector database...")

    #Run ingestion
    store = ingest_main()

    if store is None:
        print("No data found. Add files in src/data/raw/")
        return

    print("System ready! Ask your questions.\n")

    #Initialize retriever
    retriever = Retriever(store)

    #Input loop
    while True:
        query = input("Ask something (type 'exit' to quit): ")

        if query.lower() == "exit":
            print("Exiting...")
            break

        results = retriever.query(query)

        print("\n Results:\n")

        if not results:
            print("No relevant results found\n")
            continue

        for i, r in enumerate(results):
            print(f"Result {i+1}:")
            print(f"Source: {r['source']}")
            print(f"Chunk: {r['chunk']}")
            print(f"Text: {r['text']}\n")


if __name__ == "__main__":
    run()