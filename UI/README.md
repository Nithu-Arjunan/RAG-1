# RAG UI (React + TypeScript)

Production-focused React UI for your existing FastAPI RAG backend.

## Features

- Document ingestion
  - Upload mode: sends multipart request to `POST /ingest/file`
- Chat querying via `POST /chat`
- Source rendering, request-level error handling, and loading states
- Responsive layout and strict TypeScript config

## Backend Compatibility

Your current backend (`src/main.py`) supports:

- `POST /ingest/file` with multipart file upload
- `POST /chat`

UI uses upload-first ingestion via `POST /ingest/file`.

## Install (you run these manually)

From project root (`C:\Users\nithu\Desktop\GenAI\RAG-1`):

```bash
cd UI
npm install
```

## Run in development

```bash
npm run dev
```

UI default URL: `http://localhost:5173`

## Build for production

```bash
npm run build
npm run preview
```

## Environment Variables

Copy `.env.example` to `.env` and edit if needed:

- `VITE_API_BASE_URL` (default `http://127.0.0.1:8000`)
- `VITE_REQUEST_TIMEOUT_MS` (default `60000`)

## Suggested Backend CORS for local dev

Allow origin: `http://localhost:5173`

