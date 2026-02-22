export type IngestResponse = {
  file: string;
  chunks: number;
  message: string;
};

export type SourceChunk = {
  id: string;
  source: string;
  page?: string;
  score: number;
  chunk_text: string;
};

export type ChatResponse = {
  answer: string;
  sources: SourceChunk[];
  retrieved?: SourceChunk[];
  reranked?: SourceChunk[];
};

export type ApiError = {
  detail?: string;
  message?: string;
};
