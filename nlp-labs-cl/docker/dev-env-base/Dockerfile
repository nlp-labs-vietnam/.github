# ─────────────────────────────────────────────────────────────────────────────
# nlp-labs-cl/docker/dev-env-base/Dockerfile
#
# Môi trường PHÁT TRIỂN — dùng cho máy local của lập trình viên.
# Bao gồm JupyterLab, debugger, profiler và toàn bộ NLP stack.
# ─────────────────────────────────────────────────────────────────────────────
ARG PYTHON_VERSION=3.11
ARG CUDA_VERSION=12.1.0

# Chọn base tuỳ theo GPU availability
# Uncomment dòng bên dưới khi dùng GPU:
# FROM nvidia/cuda:${CUDA_VERSION}-cudnn8-devel-ubuntu22.04 AS dev-env
FROM python:${PYTHON_VERSION} AS dev-env

LABEL org.opencontainers.image.source="https://github.com/nlp-labs-vietnam/nlp-labs-cl"
LABEL org.opencontainers.image.vendor="NLP Labs Vietnam"
LABEL org.opencontainers.image.description="Full developer environment — NLP Labs Vietnam"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/workspace/.cache/huggingface \
    TRANSFORMERS_CACHE=/workspace/.cache/huggingface/transformers \
    JUPYTER_PORT=8888

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
        wget \
        vim \
        htop \
        libgomp1 \
        libopenblas-dev \
        jq \
        # Port forwarding utilities
        socat \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

# ── Core NLP Stack ─────────────────────────────────────────────────────────
RUN pip install \
    torch==2.3.0 \
    transformers==4.41.0 \
    sentence-transformers==3.0.0 \
    langchain==0.2.0 \
    langchain-community==0.2.0 \
    langchain-openai==0.1.7 \
    chromadb==0.5.0 \
    faiss-cpu==1.8.0 \
    underthesea==6.8.4 \
    pyvi==0.1.1

# ── Dev & Jupyter Tools ────────────────────────────────────────────────────
RUN pip install \
    jupyterlab==4.2.0 \
    ipywidgets==8.1.2 \
    ruff==0.4.4 \
    black==24.4.2 \
    mypy==1.10.0 \
    pytest==8.2.0 \
    pytest-cov==5.0.0 \
    pytest-asyncio==0.23.7 \
    debugpy==1.8.1

WORKDIR /workspace

RUN mkdir -p /workspace/.cache/huggingface

EXPOSE ${JUPYTER_PORT} 5678

# VS Code Remote SSH & Jupyter entrypoint
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
