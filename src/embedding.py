import os
import time
from typing import Any, Dict, List
from pinecone import Pinecone
from config import(
    PINECONE_API_KEY,
    PINECONE_CLOUD,
    PINECONE_EMBED_MODEL,
    PINECONE_INDEX_NAME,
    PINECONE_NAMESPACE,
    PINECONE_REGION,
    PINECONE_RERANK_MODEL
)

# Step1 : Connect to Pinecone

_pc = Pinecone(api_key=PINECONE_API_KEY)

def _get_or_create_index():

    if not _pc.has_index(PINECONE_INDEX_NAME):
        print(f"Creating pinecone index {PINECONE_INDEX_NAME} with integrated embedding")

        _pc.create_index_for_model(
            name=PINECONE_INDEX_NAME,
            cloud=PINECONE_CLOUD,
            region=PINECONE_REGION,
            embed={
                "model": PINECONE_EMBED_MODEL,
                "field_map": {"text": "chunk_text"},
            },
        )
        print("Index created")

        while not _pc.describe_index(PINECONE_INDEX_NAME).status.get("ready",False):
            time.sleep(1)

        print("Index created and ready")

    return _pc.Index(PINECONE_INDEX_NAME)

def is_file_ingested(source: str) -> bool:
    index = _get_or_create_index()
    try:
        # IDs are written as "<source> :: chunk-<n>", so probing chunk-1 is a stable duplicate check.
        probe_id = f"{source} :: chunk-1"
        results = index.fetch(ids=[probe_id], namespace=PINECONE_NAMESPACE)

        # Pinecone client may return a dict or a response object depending on SDK version.
        payload: Dict[str, Any]
        if isinstance(results, dict):
            payload = results
        elif hasattr(results, "to_dict"):
            payload = results.to_dict()
        elif hasattr(results, "model_dump"):
            payload = results.model_dump()
        else:
            payload = {}

        vectors = payload.get("vectors", {})
        if isinstance(vectors, dict) and probe_id in vectors:
            return True

        # Fallback for data previously inserted without stable IDs:
        # some SDK versions support filters only inside the query object.
        search_results = index.search(
            namespace=PINECONE_NAMESPACE,
            query={
                "top_k": 1,
                "inputs": {"text": source},
                "filter": {"source": source},
            },
            fields=["source"],
        )

        if isinstance(search_results, dict):
            search_payload = search_results
        elif hasattr(search_results, "to_dict"):
            search_payload = search_results.to_dict()
        elif hasattr(search_results, "model_dump"):
            search_payload = search_results.model_dump()
        else:
            search_payload = {}

        hits = search_payload.get("result", {}).get("hits", [])
        if hits:
            return True
    except Exception as exc:
        print(f"Duplicate-check failed for source '{source}': {exc}")
    return False

# Upserting records to Pinecone

def upsert_chunks(records: List[Dict], batch_size: int) -> int:
    if not records:
        return 0
    
    source=records[0].get('source',"")

    if source and is_file_ingested(source):
        print(f"{source} already exists in the Index. Skip Ingestion")
        return 0

    index=_get_or_create_index()

    total=0

    for i in range(0,len(records),batch_size):
        batch=records[i:i+batch_size]

        pinecone_records=[]

        for rec in batch:
            pinecone_records.append({
                # upsert_records expects "_id"; using "id" can lead to auto-generated IDs.
                "_id": rec['id'],
                "chunk_text": rec['chunk_text'],
                "source": rec['source'],
                "page": rec.get('page', "")
            })

        index.upsert_records(PINECONE_NAMESPACE,pinecone_records)
        total+=len(pinecone_records)

    print(f"Upserted {total} records into {PINECONE_NAMESPACE}")

    return total

# if __name__ == "__main__":
#     test_records = [
#         {"id": "test::chunk_0", "chunk_text": "This is a test chunk", "source": "test1_pdf", "page": "1"},
#         {"id": "test::chunk_1", "chunk_text": "This is a test chunk", "source": "test2_pdf", "page": "2"},
#         {"id": "test::chunk_2", "chunk_text": "This is a test chunk", "source": "test3_pdf", "page": "3"},
#     ]

#     # test_records=[
#     #     {'id': 'HR_Handbook.pdf :: chunk-1', 'chunk_text': 'AlturaTech Solutions Pvt. Ltd. Employee Lifecycle & Benefits Handbook – Internal Use Only Version 4.0 | Updated: March 2025 1. Probation, Confirmation & Role Paths All new employees are on a mandatory 4-month probation with evaluation checkpoints at 30, 75, and 120 days. Specifics: • Tech Associates (L1-L3): Must complete two internal project audits and maintain at least 85% on OKR tracking to be confirmed. • Support Roles (HR, Finance, Admin): Evaluation includes a culture-fit review and one shadow-assist', 'source': 'HR_Handbook.pdf', 'pages': '1'}, {'id': 'HR_Handbook.pdf :: chunk-2', 'chunk_text': 'Evaluation includes a culture-fit review and one shadow-assist report. • Managerial Tracks: 360-degree feedback and leadership simulation session mandatory before confirmation. Confirmation letters are issued via the TalentStream portal, not email. Status auto-updates to internal dashboards after final panel. 2. Leave Policy (Non-Public Perks) Leave structure is tenure-weighted: Tenure Casual Leave Earned Leave Remote Work Days <1 year 8/year 10/year 12/year 1–3 years 10/year 15/year 24/year >3 years 12/ye', 'source': 'HR_Handbook.pdf', 'pages': '1'}
#     # ]

#     count = upsert_chunks(test_records, batch_size=100)



    
   






