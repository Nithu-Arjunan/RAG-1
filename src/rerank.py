from typing import List,Dict
from pinecone import Pinecone

from retrieval import search
from config import(
    PINECONE_API_KEY,
    PINECONE_CLOUD,
    PINECONE_EMBED_MODEL,
    PINECONE_INDEX_NAME,
    PINECONE_NAMESPACE,
    PINECONE_REGION,
    PINECONE_RERANK_MODEL,
    TOP_K,
    RERANK_TOP_N
)

_pc=Pinecone(api_key=PINECONE_API_KEY)

def rerank(query: str, top_k: int = TOP_K,top_n: int = RERANK_TOP_N) -> List[Dict]:
    index=_pc.Index(PINECONE_INDEX_NAME)

    results=index.search(
        namespace=PINECONE_NAMESPACE,
        query={"top_k":top_k,"inputs":{"text":query}},
        rerank={"model":PINECONE_RERANK_MODEL,"top_n":top_n,"rank_fields":["chunk_text"]},
        fields=["chunk_text","source","pages"]
    )

    print(results)

    hits=[]

    for item in results.get("result", {}).get("hits", []):
        fields = item.get("fields", {})
        # Prefer 'score' from fields, then top-level '_score', then 0
        score = fields.get("score")
        if score is None:
            score = item.get("_score", 0)
        hits.append(
            {
                "id": fields.get("id", ""),
                "score": score,
                "chunk_text": fields.get("chunk_text", ""),
                "source": fields.get("source", ""),
                "page": fields.get("pages", "")
            }
        )

    return hits

if __name__ == "__main__":
    import sys

    print("=== Reranker Test ===")
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is employee lifecycle?"
    print(f"Query: {query}\n")

    results = rerank(query, top_k=5, top_n=3)
    print(f"Reranked {len(results)} results:\n")
    for i, r in enumerate(results, 1):
        print(f"  [{i}] score={r['score']} | source={r['source']} | page={r['page']}")
        print(f"      {r['chunk_text'][:150]}...\n")
    print("✅ Reranker test passed!")

