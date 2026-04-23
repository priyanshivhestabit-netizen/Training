from sentence_transformers import SentenceTransformer,util

model = SentenceTransformer("BAAI/bge-small-en")

def rerank(query,results):
    query_emb = model.encode(query, convert_to_tensor=True)

    scored=[]

    for item in results:
        doc_emb = model.encode(item["text"],convert_to_tensor=True)
        score = util.cos_sim(query_emb, doc_emb).item()

        scored.append((item,score))

    #sort by similarity
    scored.sort(key=lambda x: x[1],reverse=True)

    return [item for item, _ in scored]