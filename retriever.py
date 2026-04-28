import jieba
from rank_bm25 import BM25Okapi
from config import TOP_K


def tokenize(text: str) -> list[str]:
    return [tok.strip() for tok in jieba.lcut(text) if tok.strip()]


def build_bm25(chunks: list[dict]):
    tokenized_chunks = [tokenize(chunk["text"]) for chunk in chunks]
    bm25 = BM25Okapi(tokenized_chunks)
    return bm25


def retrieve(query: str, bm25, chunks: list[dict], top_k: int = TOP_K):
    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    indexed_scores = list(enumerate(scores))
    indexed_scores.sort(key=lambda x: x[1], reverse=True)

    results = []
    for idx, score in indexed_scores[:top_k]:
        item = chunks[idx]
        results.append({
            "rank": len(results) + 1,
            "score": float(score),
            "source": item["source"],
            "chunk_id": item["chunk_id"],
            "text": item["text"]
        })
    return results
