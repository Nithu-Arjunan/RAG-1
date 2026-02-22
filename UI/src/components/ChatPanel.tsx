import { FormEvent, useState } from "react";
import { queryChat } from "../lib/api";
import type { ChatResponse } from "../types/api";
import { SourceList } from "./SourceList";

export function ChatPanel() {
  const [query, setQuery] = useState("");
  const [useReranker, setUseReranker] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ChatResponse | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = query.trim();
    if (!trimmed || isLoading) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await queryChat(trimmed, useReranker);
      setResult(response);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unable to fetch answer";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Ask Questions</h2>
        <p>Query the ingested document collection.</p>
      </div>

      <form className="chat-form" onSubmit={handleSubmit}>
        <label htmlFor="query-input">Your question</label>
        <textarea
          id="query-input"
          rows={4}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="What are the top sales objection handling steps?"
        />

        <label className="check-row" htmlFor="reranker-checkbox">
          <input
            id="reranker-checkbox"
            type="checkbox"
            checked={useReranker}
            onChange={(event) => setUseReranker(event.target.checked)}
          />
          Use reranker
        </label>

        <button className="primary" type="submit" disabled={isLoading || !query.trim()}>
          {isLoading ? "Thinking..." : "Ask"}
        </button>
      </form>

      {error ? <p className="error">{error}</p> : null}

      {result ? (
        <div className="answer-wrap">
          <h3>Answer</h3>
          <p>{result.answer}</p>
          <SourceList sources={result.sources ?? []} />
        </div>
      ) : null}
    </section>
  );
}
