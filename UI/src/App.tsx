import { useState } from "react";
import { ChatPanel } from "./components/ChatPanel";
import { DocumentIngestPanel } from "./components/DocumentIngestPanel";
import { IngestStatus } from "./components/IngestStatus";
import type { IngestResponse } from "./types/api";

function App() {
  const [ingestResult, setIngestResult] = useState<IngestResponse | null>(null);

  return (
    <main className="app-shell">
      <header className="hero">
        <p className="eyebrow">RAG Console</p>
        <h1>Document Intelligence Workspace</h1>
        <p>Ingest documents and ask questions against your knowledge base.</p>
      </header>

      <IngestStatus result={ingestResult} />

      <section className="grid">
        <DocumentIngestPanel onIngested={setIngestResult} />
        <ChatPanel />
      </section>
    </main>
  );
}

export default App;
