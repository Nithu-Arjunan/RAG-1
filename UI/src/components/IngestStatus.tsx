import type { IngestResponse } from "../types/api";

type Props = {
  result: IngestResponse | null;
};

export function IngestStatus({ result }: Props) {
  if (!result) {
    return (
      <div className="status-banner neutral">
        <strong>Status:</strong> No document ingested in this session.
      </div>
    );
  }

  const skipped = result.chunks === 0;

  return (
    <div className={`status-banner ${skipped ? "neutral" : "success"}`}>
      <strong>Last Ingestion:</strong> {result.file} ({result.chunks} chunks) - {result.message}
    </div>
  );
}
