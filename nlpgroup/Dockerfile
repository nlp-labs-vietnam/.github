# ─────────────────────────────────────────────────────────────────────────────
# nlpgroup/Dockerfile
# Production image cho Solar AI Advisor API
# Build: docker build -t ghcr.io/nlp-labs-vietnam/nlpgroup:latest .
# ─────────────────────────────────────────────────────────────────────────────

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base

LABEL org.opencontainers.image.source="https://github.com/nlp-labs-vietnam/nlpgroup"
LABEL org.opencontainers.image.vendor="NLP Labs Vietnam"
LABEL org.opencontainers.image.description="Solar AI Advisor API — NLP Labs Vietnam"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    # nlp-labs-cl được mount hoặc copy vào đây
    PYTHONPATH="/app:/app/nlp-labs-cl" \
    HF_HOME="/app/.cache/huggingface"

# Runtime system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgomp1 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd --gid 1001 nlpuser \
    && useradd --uid 1001 --gid nlpuser --shell /bin/bash --create-home nlpuser

WORKDIR /app

# ── Cài dependencies ──────────────────────────────────────────────────────────
# Stage 1: chỉ copy requirements để tận dụng Docker layer cache
COPY requirements.txt ./
# nlp-labs-cl runtime deps
COPY ../nlp-labs-cl/requirements.txt ./nlp-labs-cl-requirements.txt
RUN pip install --no-cache-dir \
    -r requirements.txt \
    -r nlp-labs-cl-requirements.txt \
    && rm nlp-labs-cl-requirements.txt

# ── Copy source code ──────────────────────────────────────────────────────────
COPY src/ ./src/
# Copy nlp-labs-cl modules (hoặc dùng volume mount khi dev)
COPY ../nlp-labs-cl/modules/ ./nlp-labs-cl/modules/

RUN mkdir -p /app/.cache/huggingface
RUN chown -R nlpuser:nlpuser /app

USER nlpuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2", \
     "--log-level", "info"]
