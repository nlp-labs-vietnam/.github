"""
src/core/config.py
───────────────────
Cấu hình ứng dụng — đọc từ biến môi trường và file .env
Dùng pydantic-settings để type-safe và validate tự động.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────────────────────
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Danh sách origins được phép CORS",
    )

    # ── LLM Provider ─────────────────────────────────────────────────────────
    LLM_PROVIDER: Literal["openai", "anthropic", "local"] = "openai"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-haiku-20240307"

    # Giới hạn chi phí — dừng nếu vượt ngưỡng (USD/ngày)
    LLM_DAILY_BUDGET_USD: float = 5.0

    # ── Embedding Model ───────────────────────────────────────────────────────
    EMBEDDING_MODEL: str = "keepitreal/vietnamese-sbert"
    EMBEDDING_DEVICE: str = "cpu"
    EMBEDDING_BATCH_SIZE: int = 32

    # ── Vector Store (ChromaDB) ───────────────────────────────────────────────
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_COLLECTION: str = "solar_knowledge_base"

    # ── RAG Pipeline ─────────────────────────────────────────────────────────
    RAG_TOP_K: int = 5
    RAG_SIMILARITY_THRESHOLD: float = 0.65
    RAG_HYBRID_SEARCH: bool = True
    RAG_BM25_WEIGHT: float = 0.3
    RAG_MAX_CONTEXT_TOKENS: int = 3000

    # ── LLM Generation ────────────────────────────────────────────────────────
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 1024
    LLM_SYSTEM_PROMPT: str = (
        "Bạn là chuyên gia tư vấn hệ thống điện mặt trời tại Việt Nam. "
        "Chỉ trả lời dựa trên tài liệu được cung cấp. "
        "Nếu không có thông tin, hãy thông báo rõ ràng thay vì bịa đặt số liệu. "
        "Trích dẫn nguồn tài liệu khi đưa ra số liệu kỹ thuật."
    )

    # ── Cache ─────────────────────────────────────────────────────────────────
    QUERY_CACHE_ENABLED: bool = True
    QUERY_CACHE_TTL: int = 3600   # seconds
    QUERY_CACHE_MAX_SIZE: int = 10_000

    @field_validator("OPENAI_API_KEY", "ANTHROPIC_API_KEY", mode="before")
    @classmethod
    def _strip_quotes(cls, v: str) -> str:
        return v.strip().strip('"').strip("'")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton — chỉ tạo Settings một lần, cache cho các lần sau."""
    return Settings()


# Import-level singleton dùng như `from src.core.config import settings`
settings = get_settings()
