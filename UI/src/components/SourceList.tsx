import type { SourceChunk } from "../types/api";

type Props = {
  sources: SourceChunk[];
};

export function SourceList({ sources }: Props) {
  if (!sources.length) {
    return null;
  }

  return (
    <div className="sources-wrap">
      <h3>Sources</h3>
      <ul className="source-list">
        {sources.map((source, index) => (
          <li key={`${source.id}-${index}`}>
            <div className="source-meta">
              <span>{source.source || "Unknown"}</span>
              <span>Score: {source.score?.toFixed?.(4) ?? source.score}</span>
              {source.page ? <span>Page: {source.page}</span> : null}
            </div>
            <p>{source.chunk_text}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
