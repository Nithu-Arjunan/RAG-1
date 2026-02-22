# syntax=docker/dockerfile:1

FROM node:20-alpine AS ui-build
WORKDIR /app/UI
COPY UI/package*.json ./
RUN npm ci
COPY UI/ ./
RUN npm run build

FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY src/ ./src/
COPY requirements.txt README.md ./
COPY --from=ui-build /app/UI/dist ./UI/dist

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "cd src && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
