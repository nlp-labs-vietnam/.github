"""
nlpgroup/src/main.py
─────────────────────
FastAPI application factory cho hệ thống tư vấn điện mặt trời thông minh.
Kết nối nlp-labs-cl modules (tokenizer, embedding, ner) với ChromaDB và LLM.

Chạy development:
    uvicorn src.main:app --reload --port 8000

Chạy production:
    uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 2
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.api.routers import chat, health, solar
from src.core.config import settings
from src.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Khởi tạo và giải phóng tài nguyên khi server start/stop."""
    setup_logging()

    # ── Startup ──────────────────────────────────────────────────────────────
    from src.core.dependencies import get_rag_pipeline  # noqa: PLC0415
    # Khởi tạo pipeline trước để warm-up embedding model
    pipeline = await get_rag_pipeline()
    app.state.rag_pipeline = pipeline

    yield

    # ── Shutdown ─────────────────────────────────────────────────────────────
    # Giải phóng kết nối ChromaDB
    if hasattr(app.state, "rag_pipeline"):
        await app.state.rag_pipeline.close()


def create_app() -> FastAPI:
    """Application factory — tạo và cấu hình FastAPI instance."""
    app = FastAPI(
        title="NLP Labs Vietnam — Solar AI Advisor",
        description=(
            "Hệ thống tư vấn, thiết kế và tối ưu hóa hệ thống điện mặt trời "
            "thông minh bằng tiếng Việt, ứng dụng công nghệ RAG và LLM."
        ),
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # ── Middleware ────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # ── Routers ───────────────────────────────────────────────────────────────
    app.include_router(health.router, tags=["Health"])
    app.include_router(chat.router,   prefix="/api/v1", tags=["Chat"])
    app.include_router(solar.router,  prefix="/api/v1", tags=["Solar"])

    return app


app = create_app()
