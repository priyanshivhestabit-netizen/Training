from collections import Counter
from src.pipelines.ingest import embed_texts

class HybridRetriever:
    def __init__(self,vectorstore):
        self.vectorstore = vectorstore

    # keyword scoring
    def keyword_score(self,query,text):
        q_words = query.lower().split()
        t_words = text.lower().split()
            
        score=0
        word_count=Counter(t_words)

        for word in q_words:
            score+=word_count[word]

        return score
        
    # main query
    def query(self,question,k=5):
        # 1.semantic search
        q_emb = embed_texts([question])
        semantic_results = self.vectorstore.search(q_emb,k*2)

        # 2.keyword scoring
        scored=[]
        for item in semantic_results:
            score = self.keyword_score(question,item["text"])
            scored.append((item,score))

        # 3.sort by keyword score
        scored.sort(key=lambda x: x[1],reverse=True)

        # 4.deduplicate
        seen=set()
        final=[]

        for item,score in scored:
            if item["text"] not in seen:
                seen.add(item["text"])
                final.append(item)

            if len(final) >=k:
                break

        return final
        