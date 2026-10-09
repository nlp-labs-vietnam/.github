"""
src/core/dependencies.py
──────────────────────────
FastAPI dependency injection — cung cấp các singleton services cho request handlers.
Dùng pattern: lru_cache singleton + FastAPI Depends().
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.core.config import Settings, get_settings
from src.rag.pipeline import RAGPipeline

logger = logging.getLogger(__name__)

# ─── Singletons ───────────────────────────────────────────────────────────────

_rag_pipeline: RAGPipeline | None = None


async def get_rag_pipeline(
    settings: Annotated[Settings, Depends(get_settings)],
) -> RAGPipeline:
    """
    Dependency: trả về RAGPipeline singleton.
    Lazy-init lần đầu tiên, tái sử dụng cho tất cả requests tiếp theo.
    """
    global _rag_pipeline
    if _rag_pipeline is None:
        logger.info("Khởi tạo RAGPipeline lần đầu...")
        _rag_pipeline = await RAGPipeline.create(settings)
        logger.info("RAGPipeline sẵn sàng")
    return _rag_pipeline


# ─── Type aliases để dùng trong route handlers ────────────────────────────────

RAGPipelineDep = Annotated[RAGPipeline, Depends(get_rag_pipeline)]
SettingsDep    = Annotated[Settings, Depends(get_settings)]
