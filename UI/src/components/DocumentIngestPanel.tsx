import { useMemo, useState } from "react";
import { ingestByFile } from "../lib/api";
import type { IngestResponse } from "../types/api";

type Props = {
  onIngested: (result: IngestResponse) => void;
};

export function DocumentIngestPanel({ onIngested }: Props) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const uploadDisabled = useMemo(() => isLoading || !selectedFile, [isLoading, selectedFile]);

  async function handleUpload() {
    if (!selectedFile) {
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const response = await ingestByFile(selectedFile);
      onIngested(response);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unable to ingest file";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Document Ingestion</h2>
        <p>Upload a document to index it for search and question answering.</p>
      </div>

      <div className="field-group">
        <label htmlFor="file-input">Choose document</label>
        <input
          id="file-input"
          type="file"
          onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
          accept=".pdf,.doc,.docx,.txt,.md"
        />
        <button className="primary" type="button" disabled={uploadDisabled} onClick={handleUpload}>
          {isLoading ? "Uploading..." : "Upload and Ingest"}
        </button>
        <small>Uploaded files are stored server-side and indexed for search.</small>
      </div>

      {error ? <p className="error">{error}</p> : null}
    </section>
  );
}
