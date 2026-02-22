import os
from dotenv import load_dotenv
load_dotenv()

# API keys

PINECONE_API_KEY=os.getenv("PINECONE_API_KEY","")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY","")

# Chunking settings

CHUNK_SIZE: int = 1000
CHUNK_OVERLAP:int = 200


# PineCone settings

PINECONE_INDEX_NAME: str = "classicragchatbot"
PINECONE_NAMESPACE: str = "documents"
PINECONE_CLOUD: str = "aws"
PINECONE_REGION: str = "us-east-1"
PINECONE_EMBED_MODEL: str = "multilingual-e5-large"  
PINECONE_RERANK_MODEL: str = "bge-reranker-v2-m3"    

# Retrieval settings

TOP_K:int = 10
RERANK_TOP_N:int = 5

# Generation settings
PROJECT_ID: str = "genaiacademy-487009"
LOCATION: str = "us-central1"
GEMINI_MODEL: str = "gemini-2.0-flash"
MAX_TOKENS: int = 1024
TEMPERATURE: float = 0.2