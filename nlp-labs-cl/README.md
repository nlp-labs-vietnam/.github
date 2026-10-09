# nlp-labs-cl

> **NLP Labs Vietnam — Core NLP Library**  
> Monorepo chứa các module NLP dùng chung cho toàn bộ hệ sinh thái AI và Năng lượng Mặt trời Việt Nam.

[![CI](https://github.com/nlp-labs-vietnam/nlp-labs-cl/actions/workflows/ci.yml/badge.svg)](https://github.com/nlp-labs-vietnam/nlp-labs-cl/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Kiến trúc tổng quan

```
nlp-labs-cl/
├── .github/
│   ├── workflows/              # CI/CD: ci.yml · build-images.yml · lint.yml
│   └── actions/                # Custom actions: setup-python-nlp · validate-nlp-data
│
├── docker/
│   ├── run-env-base/           # Runtime image (production inference)
│   ├── build-env-base/         # Build & CI image
│   ├── dev-env-base/           # Developer image (JupyterLab + full stack)
│   └── docker-compose.yml      # Local development stack
│
├── modules/                    # ← Các thành phần NLP modular
│   ├── tokenizer/              # Phân tách từ tiếng Việt (underthesea/pyvi/whitespace)
│   ├── embedding/              # Dense vector embeddings (SentenceTransformer)
│   └── ner/                    # Nhận dạng thực thể Solar domain (rule_based/model)
│
├── configs/
│   ├── training/               # Cấu hình fine-tuning models
│   ├── inference/              # Cấu hình RAG pipeline
│   └── pipeline/               # Cấu hình chạy toàn bộ pipeline
│
├── scripts/
│   ├── build_env.py            # Chuẩn bị môi trường phát triển
│   ├── run_pipeline.py         # Chạy NLP pipeline từ config
│   └── validate_configs.py     # Kiểm tra tính hợp lệ của configs
│
├── requirements.txt            # Runtime dependencies
├── requirements-dev.txt        # Dev/CI dependencies
└── pyproject.toml              # Project config (ruff, black, mypy, pytest)
```

---

## Bắt đầu nhanh

### 1. Clone & Setup

```bash
git clone https://github.com/nlp-labs-vietnam/nlp-labs-cl.git
cd nlp-labs-cl

# Tự động setup toàn bộ môi trường
python scripts/build_env.py

# Hoặc chỉ setup một module cụ thể
python scripts/build_env.py --module tokenizer
```

### 2. Dùng Docker (khuyến nghị)

```bash
# Khởi động toàn bộ dev stack (JupyterLab + ChromaDB + API)
cd docker
docker compose up -d

# JupyterLab tại: http://localhost:8888
# API tại:        http://localhost:8000
# ChromaDB tại:   http://localhost:8001
```

### 3. Sử dụng từng module

```python
# Tokenizer
from modules.tokenizer import VietnameseTokenizer

tokenizer = VietnameseTokenizer({"backend": "underthesea"})
tokens = tokenizer.tokenize("Hệ thống điện mặt trời 5 kWp tại Hà Nội")
# → ["Hệ thống", "điện", "mặt trời", "5", "kWp", "tại", "Hà Nội"]

# Embedding
from modules.embedding import VietnameseEmbedder

embedder = VietnameseEmbedder({"model_name": "keepitreal/vietnamese-sbert"})
vectors = embedder.embed(["Điện mặt trời", "Năng lượng tái tạo"])
# → numpy array (2, 768)

# NER
from modules.ner import SolarNERExtractor

extractor = SolarNERExtractor({"mode": "rule_based"})
entities = extractor.extract("Lắp 5 kWp Growatt tại Hà Nội giá 80 triệu đồng")
# → [Entity(text="5 kWp", label="CAPACITY"), Entity(text="Growatt", label="BRAND"), ...]
```

### 4. Chạy pipeline đầy đủ

```bash
python scripts/run_pipeline.py --config configs/pipeline/solar-qa.yml
```

---

## Chạy kiểm thử

```bash
# Toàn bộ test suite
pytest

# Một module cụ thể
pytest modules/tokenizer/tests/ -v
pytest modules/embedding/tests/ -v
pytest modules/ner/tests/ -v

# Với coverage report
pytest --cov=modules --cov-report=html
```

---

## Đóng gói Docker Images

```bash
# Build tất cả images (local)
python scripts/build_env.py --docker

# Hoặc chỉ build một image
docker build -t nlp-labs-cl/dev-env:local docker/dev-env-base/
```

---

## Cấu trúc CI/CD

| Workflow | Kích hoạt | Mô tả |
|---|---|---|
| `ci.yml` | push/PR → main, develop | Lint + Test ma trận Python 3.10/3.11 + Integration test |
| `build-images.yml` | push → main (docker/) | Build & push 3 Docker images lên ghcr.io |
| `lint.yml` | PR → main (*.py files) | Ruff + Black + Mypy + Config validation |

---

## Đóng góp

Xem [CONTRIBUTING.md](https://github.com/nlp-labs-vietnam/.github/blob/main/CONTRIBUTING.md) để biết quy trình đóng góp của tổ chức.

---

## License

MIT © [NLP Labs Vietnam](https://nlpgroup.vn)
