# RAG-1

Retrieval-Augmented Generation (RAG) app with:
- FastAPI backend for document ingestion and chat querying
- React + TypeScript UI in `UI/` for upload and query workflows
- Single-service deployment option for Cloud Run (UI + API in one container)

## Current Stack

- Backend: FastAPI, Pinecone, Gemini
- Frontend: React 18, TypeScript, Vite

## Project Structure

```text
RAG-1/
  src/                 # Backend source
  docs/                # Input/sample docs (+ runtime uploads)
  UI/                  # React TypeScript frontend
  Dockerfile           # Single-container build for Cloud Run
  .dockerignore
  pyproject.toml
  README.md
```

## Backend API

- `GET /health`
- `POST /ingest` (optional path-based ingestion)
- `POST /ingest/file` (multipart upload; used by UI)
- `POST /chat`

## Local Development

Backend:

```bash
cd src
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd UI
npm install
npm run dev
```

For local split-run, set `UI/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Single App Deployment (Cloud Run)

This repo is set up to deploy UI + API as one Cloud Run service using `Dockerfile`.

1. Set your project/region:

```bash
gcloud config set project <YOUR_GCP_PROJECT_ID>
gcloud config set run/region <YOUR_REGION>
```

2. Build and deploy:

```bash
gcloud run deploy rag-1 \
  --source . \
  --platform managed \
  --allow-unauthenticated
```

3. Configure environment variables/secrets in Cloud Run:
- `PINECONE_API_KEY`



