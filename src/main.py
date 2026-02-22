from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List, Optional
from ingestion import ingest_document
from embedding import upsert_chunks
from retrieval import search
from rerank import rerank
from generation import generate_answer

app = FastAPI(title='RAG chatbot',
               description='A chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions based on ingested documents.')

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("docs") / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
UI_DIST_DIR = Path(__file__).resolve().parents[1] / "UI" / "dist"

class IngestRequest(BaseModel):
    file_path: str

class IngestResponse(BaseModel):
    file: str
    chunks: int
    message: str

class ChatRequest(BaseModel):
    query: str
    use_reranker: bool = True
    debug: bool = False

class SourceChunks(BaseModel):
    id: str
    source: str
    chunk_text: str
    page: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunks]
    retrieved: Optional[List[SourceChunks]] = None
    reranked: Optional[List[SourceChunks]] = None

class GenerateRequest(BaseModel):
    query: str
    top_k: int = 10
    top_n: int = 5
    reranker: bool = True

class GenerateResponse(BaseModel):
    query: str
    answer: str
    sources: List[SourceChunks]
    pipeline: str

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 10
    reranker: bool = True

# Add API endpoints

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest):
    try:
        chunks = ingest_document(request.file_path)
        count = upsert_chunks(chunks, batch_size=100)
        if count == 0:
            return IngestResponse(file=request.file_path, chunks=count, message="File is already ingested. Proceed to query the document.")
        return IngestResponse(file=request.file_path, chunks=count, message="Ingestion successful")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest/file", response_model=IngestResponse)
async def ingest_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided")

    try:
        destination = UPLOAD_DIR / Path(file.filename).name
        file_bytes = await file.read()
        destination.write_bytes(file_bytes)

        chunks = ingest_document(str(destination))
        count = upsert_chunks(chunks, batch_size=100)
        if count == 0:
            return IngestResponse(file=str(destination), chunks=count, message="File is already ingested. Proceed to query the document.")
        return IngestResponse(file=str(destination), chunks=count, message="Ingestion successful")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        retrieved_chunks = search(request.query, top_k=10)

        if request.use_reranker:
            reranked_chunks = rerank(request.query, top_k=10, top_n=5)
            answer = generate_answer(request.query, reranked_chunks)
            return ChatResponse(answer=answer, sources=reranked_chunks, reranked=reranked_chunks)
        else:
            answer = generate_answer(request.query, retrieved_chunks)
            return ChatResponse(answer=answer, sources=retrieved_chunks, retrieved=retrieved_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", include_in_schema=False)
def serve_ui_index():
    if UI_DIST_DIR.exists():
        return FileResponse(UI_DIST_DIR / "index.html")
    raise HTTPException(status_code=404, detail="UI build not found")

@app.get("/{full_path:path}", include_in_schema=False)
def serve_ui_assets(full_path: str):
    if full_path.startswith(("health", "ingest", "chat", "docs", "openapi.json", "redoc", "swagger")):
        raise HTTPException(status_code=404, detail="Not found")

    if not UI_DIST_DIR.exists():
        raise HTTPException(status_code=404, detail="UI build not found")

    requested = (UI_DIST_DIR / full_path).resolve()
    try:
        requested.relative_to(UI_DIST_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")

    if requested.is_file():
        return FileResponse(requested)

    return FileResponse(UI_DIST_DIR / "index.html")
