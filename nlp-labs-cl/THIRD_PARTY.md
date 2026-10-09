# THIRD_PARTY.md — Thư viện và Mã nguồn Bên thứ ba

Tài liệu này liệt kê tất cả thư viện mã nguồn mở được sử dụng trong `nlp-labs-cl`, cùng với giấy phép của chúng.

---

## Thư viện NLP & AI

| Thư viện | Phiên bản | Giấy phép | Tác giả / Tổ chức |
|---|---|---|---|
| [PyTorch](https://pytorch.org) | ≥2.3.0 | BSD-3-Clause | Meta AI Research |
| [Transformers](https://huggingface.co/transformers) | ≥4.41.0 | Apache 2.0 | HuggingFace |
| [sentence-transformers](https://sbert.net) | ≥3.0.0 | Apache 2.0 | UKP Lab, TU Darmstadt |
| [LangChain](https://langchain.com) | ≥0.2.0 | MIT | LangChain, Inc. |
| [ChromaDB](https://trychroma.com) | ≥0.5.0 | Apache 2.0 | Chroma |
| [FAISS](https://faiss.ai) | ≥1.8.0 | MIT | Meta AI Research |

---

## Thư viện NLP Tiếng Việt

| Thư viện | Phiên bản | Giấy phép | Tác giả |
|---|---|---|---|
| [underthesea](https://github.com/undertheseanlp/underthesea) | ≥6.8.4 | GPL-3.0 | Vu Anh, undertheseanlp |
| [pyvi](https://github.com/trungtv/pyvi) | ≥0.1.1 | MIT | Trung Tran |

> ⚠️ **Lưu ý quan trọng:** `underthesea` được cấp phép theo **GPL-3.0**. Nếu bạn phân phối phần mềm có nhúng thư viện này, toàn bộ mã nguồn phải được công khai theo GPL-3.0. Để triển khai dạng API không cần mở mã nguồn, hãy dùng backend `pyvi` hoặc `whitespace`.

---

## Models đã sử dụng

| Model | Nguồn | Giấy phép | Mô tả |
|---|---|---|---|
| [keepitreal/vietnamese-sbert](https://huggingface.co/keepitreal/vietnamese-sbert) | HuggingFace Hub | Apache 2.0 | SentenceTransformer tiếng Việt |
| [VoVanPhuc/sup-SimCSE-Viet-roberta-base](https://huggingface.co/VoVanPhuc/sup-SimCSE-Viet-roberta-base) | HuggingFace Hub | MIT | SimCSE Vietnamese |
| [NlpHUST/ner-vietnamese-electra-base](https://huggingface.co/NlpHUST/ner-vietnamese-electra-base) | HuggingFace Hub | MIT | NER tiếng Việt |

---

## Thư viện API & Web

| Thư viện | Phiên bản | Giấy phép |
|---|---|---|
| [FastAPI](https://fastapi.tiangolo.com) | ≥0.111.0 | MIT |
| [Uvicorn](https://www.uvicorn.org) | ≥0.29.0 | BSD-3-Clause |
| [Pydantic](https://docs.pydantic.dev) | ≥2.7.0 | MIT |

---

## Công cụ Phát triển (Dev Dependencies)

| Công cụ | Giấy phép | Mục đích |
|---|---|---|
| [Ruff](https://docs.astral.sh/ruff) | MIT | Linter |
| [Black](https://black.readthedocs.io) | MIT | Code formatter |
| [Mypy](https://mypy.readthedocs.io) | MIT | Type checker |
| [pytest](https://pytest.org) | MIT | Test framework |
| [pip-audit](https://pypi.org/project/pip-audit) | Apache 2.0 | Vulnerability scanner |

---

## Hạ tầng & DevOps

| Công cụ | Giấy phép |
|---|---|
| GitHub Actions | [GitHub Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) |
| Docker | Apache 2.0 |
| [Trivy](https://trivy.dev) (scanner) | Apache 2.0 |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | AGPL-3.0 |

---

*Cập nhật lần cuối: 2025. Để báo cáo vấn đề giấy phép, liên hệ `contact@nlpgroup.vn`.*
