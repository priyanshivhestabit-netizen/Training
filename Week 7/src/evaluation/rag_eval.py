from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("BAAI/bge-small-en")

def context_match_score(answer,context_chunks):
    if not context_chunks or not answer:
        return 0.0
    
    answer_emb = model.encode(answer,convert_to_tensor=True)

    scores=[]
    for chunk in context_chunks:
        chunk_text =chunk.get("text","") if isinstance(chunk,dict) else str(chunk)

        if not chunk_text.strip():
            continue
        chunk_emb=model.encode(chunk_text[:500],convert_to_tensor=True)
        score =util.cos_sim(answer_emb, chunk_emb).item()

        scores.append(score)

    if not scores:
        return 0.0
    
    return round(max(scores),3)

def detect_hallucination(answer, context_chunks, threshold=0.35):
    score = context_match_score(answer, context_chunks)

    if score >= 0.5:
        label = "FAITHFUL"
        hallucinated = False
    elif score >= threshold:
        label = "PARTIAL"
        hallucinated= False
    else:
        label = "HALLUCINATED"
        hallucinated = True
    return hallucinated, score, label

def confidence_score(answer, context_chunks):
    base_score = context_match_score(answer, context_chunks)

    #penalty
    if(len(answer.split())<5):
        base_score*=0.7

    uncertainty_phrases = ["i don't know","i am not sure","cannot determine","no information","unclear","not available"] 
    
    if any(p in answer.lower() for p in uncertainty_phrases):
        base_score *= 0.6

    confidence_pct = round(min(base_score * 100,100),1)
    return confidence_pct

def evaluate(answer, context_chunks):
    hallucinated, faith_score , label = detect_hallucination(answer, context_chunks)
    conf = confidence_score(answer, context_chunks)

    return {
        "faithfulness_score": faith_score,
        "hallucination_label": label,
        "is_hallucinated": hallucinated,
        "confidence_pct": conf
    }

