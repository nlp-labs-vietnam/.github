"""
src/rag/pipeline.py
────────────────────
RAG Pipeline — điều phối toàn bộ luồng: embed → retrieve → generate.
Là entry point duy nhất cho tầng API sử dụng.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import AsyncIterator

from src.core.config import Settings
from src.rag.generator import Generator
from src.rag.retriever import RetrievedDoc, Retriever

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Kết quả trả về từ RAG pipeline."""
    answer: str
    citations: list[dict] = field(default_factory=list)
    retrieved_docs: list[RetrievedDoc] = field(default_factory=list)
    query: str = ""


class RAGPipeline:
    """
    Điều phối toàn bộ RAG pipeline:
      1. Embed query (nlp-labs-cl embedding module)
      2. Retrieve relevant docs (ChromaDB)
      3. Generate answer (LLM via Generator)
      4. Format citations

    Không khởi tạo trực tiếp — dùng `RAGPipeline.create(settings)`.
    """

    def __init__(self, settings: Settings, retriever: Retriever, generator: Generator) -> None:
        self.settings = settings
        self.retriever = retriever
        self.generator = generator

    @classmethod
    async def create(cls, settings: Settings) -> "RAGPipeline":
        """
        Factory method — khởi tạo embedding model, ChromaDB client, LLM client.
        Gọi một lần duy nhất khi server start.
        """
        # Nạp embedding module từ nlp-labs-cl
        try:
            import sys  # noqa: PLC0415
            import os   # noqa: PLC0415
            # Thêm nlp-labs-cl vào path nếu chạy trong monorepo
            nlp_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "nlp-labs-cl")
            if os.path.exists(nlp_path) and nlp_path not in sys.path:
                sys.path.insert(0, nlp_path)

            from modules.embedding import VietnameseEmbedder  # noqa: PLC0415
            embedder = VietnameseEmbedder({
                "model_name": settings.EMBEDDING_MODEL,
                "device": settings.EMBEDDING_DEVICE,
                "batch_size": settings.EMBEDDING_BATCH_SIZE,
            })
            logger.info("Embedding model loaded: %s", settings.EMBEDDING_MODEL)
        except ImportError:
            logger.warning("nlp-labs-cl không có trong PATH — dùng mock embedder")
            from src.rag._mock_embedder import MockEmbedder  # noqa: PLC0415
            embedder = MockEmbedder()

        retriever = await Retriever.create(settings, embedder)
        generator = Generator(settings)

        logger.info("RAGPipeline sẵn sàng — provider=%s", settings.LLM_PROVIDER)
        return cls(settings, retriever, generator)

    async def run(
        self,
        query: str,
        history: list[dict] | None = None,
    ) -> PipelineResult:
        """
        Chạy toàn bộ pipeline và trả về kết quả.

        Args:
            query: Câu hỏi của người dùng.
            history: Lịch sử hội thoại (danh sách {"role": ..., "content": ...}).

        Returns:
            PipelineResult với answer và citations.
        """
        logger.info("pipeline.run: query=%r", query[:80])

        # 1. Retrieve
        docs = await self.retriever.retrieve(query)

        # 2. Generate
        answer = await self.generator.generate(query, docs, history)

        # 3. Format citations
        citations = [
            {
                "title": doc.title,
                "source": doc.source,
                "year": doc.year,
                "page": doc.page,
                "score": doc.score,
            }
            for doc in docs
        ]

        return PipelineResult(
            answer=answer,
            citations=citations,
            retrieved_docs=docs,
            query=query,
        )

    async def stream(
        self,
        query: str,
        history: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """Streaming version — yield từng text chunk."""
        docs = await self.retriever.retrieve(query)
        async for chunk in self.generator.stream(query, docs, history):
            yield chunk

    async def close(self) -> None:
        """Giải phóng tài nguyên khi server shutdown."""
        await self.retriever.close()
        logger.info("RAGPipeline đã đóng kết nối")
