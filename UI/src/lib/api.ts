import type { ApiError, ChatResponse, IngestResponse } from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
const REQUEST_TIMEOUT_MS = Number(import.meta.env.VITE_REQUEST_TIMEOUT_MS ?? 60000);

type RequestOptions = {
  method?: "GET" | "POST";
  body?: BodyInit | string;
  headers?: Record<string, string>;
};

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      method: options.method ?? "GET",
      headers: options.headers,
      body: options.body,
      signal: controller.signal
    });

    if (!response.ok) {
      let errorMessage = `Request failed (${response.status})`;
      try {
        const payload = (await response.json()) as ApiError;
        errorMessage = payload.detail ?? payload.message ?? errorMessage;
      } catch {
        // Keep generic message when backend doesn't return JSON.
      }
      throw new Error(errorMessage);
    }

    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error(`Request timed out after ${REQUEST_TIMEOUT_MS}ms`);
    }
    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export function ingestByFile(file: File): Promise<IngestResponse> {
  const formData = new FormData();
  formData.append("file", file);

  return request<IngestResponse>("/ingest/file", {
    method: "POST",
    body: formData
  });
}

export function queryChat(query: string, useReranker: boolean): Promise<ChatResponse> {
  return request<ChatResponse>("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      use_reranker: useReranker,
      debug: false
    })
  });
}
