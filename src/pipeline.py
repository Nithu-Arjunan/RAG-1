import os
from ingestion import ingest_document
from embedding import upsert_chunks
from rerank import rerank
from generation import generate_answer

def main():
    # 1. Ingest document
    # Ask user for PDF file path
    pdf_path = input("Enter the path to the PDF file to ingest: ").strip()
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    print("1) Ingesting document...")
    records = ingest_document(pdf_path)
    print(f"Ingested {len(records)} chunks")

    # 2. Embedding/upsert
    print("2) Upserting records to Pinecone index...")
    count = upsert_chunks(records, batch_size=100)
    print(f"Upserted {count} records to Pinecone")

    # Ask user for query
    query = input("Enter your query for the document: ").strip()
    if not query:
        print("No query provided.")
        return

    # 3. Rerank/search
    print("3) Running rerank/search for your query...")
    search_results = rerank(query)
    print(f"Rerank results (top 5):")
    for r in search_results[:5]:
        print(f"- id={r.get('id')} score={r.get('score')} source={r.get('source')} page={r.get('page')}")

    # 4. Generation
    print("4) Generating answer from reranked context...")
    answer = generate_answer(query, search_results)
    print("\nGenerated answer:\n", answer)

if __name__ == "__main__":
    main()
