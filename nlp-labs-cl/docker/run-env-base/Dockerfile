# ─────────────────────────────────────────────────────────────────────────────
# nlp-labs-cl/docker/run-env-base/Dockerfile
#
# Môi trường CHẠY (Runtime) — image tối thiểu để triển khai sản xuất
# Không chứa build tools, chỉ có những gì cần thiết để chạy inference.
# ─────────────────────────────────────────────────────────────────────────────
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base

LABEL org.opencontainers.image.source="https://github.com/nlp-labs-vietnam/nlp-labs-cl"
LABEL org.opencontainers.image.vendor="NLP Labs Vietnam"
LABEL org.opencontainers.image.description="Runtime base image for NLP inference"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Cài đặt runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgomp1 \
        libopenblas0 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Tạo non-root user để chạy ứng dụng
RUN groupadd --gid 1001 nlpuser \
    && useradd --uid 1001 --gid nlpuser --shell /bin/bash --create-home nlpuser

WORKDIR /app

# Copy và cài runtime dependencies trước (tận dụng Docker layer cache)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER nlpuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
