# nlpgroup

> **NLP Labs Vietnam — Solar AI Advisor API**  
> API server FastAPI kết nối `nlp-labs-cl` modules với ChromaDB và LLM để tư vấn điện mặt trời thông minh bằng tiếng Việt.

[![CI](https://github.com/nlp-labs-vietnam/nlpgroup/actions/workflows/ci.yml/badge.svg)](https://github.com/nlp-labs-vietnam/nlpgroup/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)

---

## Kiến trúc hệ thống

```
Người dùng
    │
    ▼
[FastAPI — nlpgroup]
    │
    ├─ POST /api/v1/chat         → RAGPipeline
    │       │
    │       ├─ Embed (nlp-labs-cl/embedding)
    │       ├─ Retrieve (ChromaDB)
    │       └─ Generate (OpenAI / Anthropic)
    │
    └─ POST /api/v1/solar/calculate  → Tính toán vật lý trực tiếp
         POST /api/v1/solar/roi      → ROI & LCOE
```

---

## Bắt đầu nhanh

### 1. Chạy bằng Docker (khuyến nghị)

```bash
# Copy và điền thông tin API key
cp .env.example .env
# Chỉnh sửa .env: thêm OPENAI_API_KEY

# Khởi động stack (API + ChromaDB)
docker compose up -d

# API docs: http://localhost:8000/docs
# ChromaDB: http://localhost:8001
```

### 2. Chạy local (development)

```bash
# Cài đặt dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Đặt nlp-labs-cl trong PYTHONPATH
export PYTHONPATH=$PYTHONPATH:../nlp-labs-cl

# Copy env file
cp .env.example .env

# Chạy server với hot reload
uvicorn src.main:app --reload --port 8000
```

---

## Sử dụng API

### Chat với AI tư vấn

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Tôi cần hệ thống điện mặt trời cho nhà tiêu thụ 400 kWh/tháng tại Đà Nẵng"}
    ]
  }'
```

**Response:**
```json
{
  "answer": "Dựa trên mức tiêu thụ 400 kWh/tháng và bức xạ tại Đà Nẵng (~4.9 kWh/m²/ngày)...",
  "citations": [
    {"index": 1, "title": "Hướng dẫn lắp điện mặt trời mái nhà", "source": "EVN", "year": "2023"}
  ],
  "latency_ms": 1250
}
```

### Tính toán hệ thống

```bash
curl -X POST http://localhost:8000/api/v1/solar/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_kwh": 400,
    "province": "Đà Nẵng",
    "available_area_m2": 50
  }'
```

**Response:**
```json
{
  "recommended_capacity_kwp": 3.4,
  "estimated_area_m2": 16.1,
  "area_sufficient": true,
  "annual_output_kwh": 4870.0,
  "co2_saved_kg_per_year": 2922.0,
  "estimated_cost_vnd_million": 51.0,
  "payback_years": 6.2
}
```

---

## Chạy kiểm thử

```bash
# Unit tests (không cần ChromaDB / LLM API)
pytest tests/ -v -m "not integration"

# Với coverage
pytest tests/ --cov=src --cov-report=html

# Integration tests (cần ChromaDB đang chạy)
pytest tests/ -m integration
```

---

## Cấu trúc thư mục

```
nlpgroup/
├── src/
│   ├── main.py              # FastAPI app factory + lifespan
│   ├── core/
│   │   ├── config.py        # Settings (pydantic-settings)
│   │   ├── dependencies.py  # FastAPI DI — RAGPipeline singleton
│   │   └── logging.py       # JSON/pretty logging setup
│   ├── api/routers/
│   │   ├── chat.py          # POST /api/v1/chat (streaming-capable)
│   │   ├── solar.py         # POST /api/v1/solar/calculate + /roi
│   │   └── health.py        # GET /health + /ready (k8s probes)
│   └── rag/
│       ├── pipeline.py      # RAGPipeline: embed → retrieve → generate
│       ├── retriever.py     # ChromaDB vector search
│       └── generator.py     # LLM generation (OpenAI / Anthropic)
├── tests/
│   ├── test_solar_router.py # Solar calculation tests (no external deps)
│   └── test_rag_pipeline.py # RAG pipeline tests (mocked)
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── pyproject.toml
```

---

## Phụ thuộc chính

| Package | Mục đích |
|---|---|
| FastAPI + Uvicorn | API framework |
| Pydantic v2 + pydantic-settings | Schema validation + config |
| ChromaDB | Vector store |
| nlp-labs-cl/embedding | Vietnamese embedding (SentenceTransformer) |
| OpenAI / Anthropic SDK | LLM generation |

---

## License

MIT © [NLP Labs Vietnam](https://nlpgroup.vn)
