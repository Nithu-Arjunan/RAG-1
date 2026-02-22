from typing import List,Dict
from pinecone import Pinecone

from config import(
    PINECONE_API_KEY,
    PINECONE_CLOUD,
    PINECONE_EMBED_MODEL,
    PINECONE_INDEX_NAME,
    PINECONE_NAMESPACE,
    PINECONE_REGION,
    PINECONE_RERANK_MODEL,
    TOP_K
)

_pc=Pinecone(api_key=PINECONE_API_KEY)

def search(query: str, top_k: int = TOP_K) -> List[Dict]:
    index=_pc.Index(PINECONE_INDEX_NAME)

    results=index.search(
        namespace=PINECONE_NAMESPACE,
        query={"top_k":top_k,"inputs":{"text":query}},
        fields=["chunk_text","source","pages"]
    )

    hits=[]

    for item in results.get("result",{}).get("hits",[]):
        fields=item.get("fields",{})
        hits.append(
            {
                "id":fields.get("id",""),
                "score":fields.get("score",0),
                "chunk_text":fields.get("chunk_text",""),
                "source":fields.get("source",""),
                "page":fields.get("pages","")
            }
        )

    return hits

# if __name__=="__main__":
#     query="What is employee handbook?"
#     search_results=search(query)
#     print(search_results)