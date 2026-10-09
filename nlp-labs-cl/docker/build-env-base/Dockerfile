# ─────────────────────────────────────────────────────────────────────────────
# nlp-labs-cl/docker/build-env-base/Dockerfile
#
# Môi trường BUILD — dùng trong CI/CD để compile, lint, test.
# Chứa đầy đủ build tools, compiler và dev dependencies.
# ─────────────────────────────────────────────────────────────────────────────
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION} AS build-env

LABEL org.opencontainers.image.source="https://github.com/nlp-labs-vietnam/nlp-labs-cl"
LABEL org.opencontainers.image.vendor="NLP Labs Vietnam"
LABEL org.opencontainers.image.description="Build & CI environment for NLP Labs Vietnam"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Hugging Face cache — mount volume này trong CI để tái sử dụng
    HF_HOME=/cache/huggingface \
    TRANSFORMERS_CACHE=/cache/huggingface/transformers

# Build tools + dev utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
        wget \
        libgomp1 \
        libopenblas-dev \
        # Công cụ phân tích
        jq \
    && rm -rf /var/lib/apt/lists/*

# Nâng cấp pip + cài build tools
RUN pip install --upgrade pip setuptools wheel build

# Cài CI/QA tools
RUN pip install \
    ruff==0.4.4 \
    black==24.4.2 \
    mypy==1.10.0 \
    pytest==8.2.0 \
    pytest-cov==5.0.0 \
    pytest-asyncio==0.23.7 \
    pip-audit==2.7.3

WORKDIR /workspace

# Tạo thư mục cache cho HF models
RUN mkdir -p /cache/huggingface

CMD ["/bin/bash"]
