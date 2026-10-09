"""
tests/test_rag_pipeline.py
───────────────────────────
Unit tests cho RAG pipeline — dùng mock retriever và mock generator.
Không cần ChromaDB hay LLM API key.
"""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.rag.pipeline import PipelineResult, RAGPipeline
from src.rag.retriever import RetrievedDoc


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_docs() -> list[RetrievedDoc]:
    return [
        RetrievedDoc(
            id="doc1",
            content="Hệ thống 5 kWp phù hợp cho hộ gia đình tiêu thụ 300 kWh/tháng.",
            score=0.92,
            metadata={"title": "Hướng dẫn lắp điện mặt trời", "source": "EVN", "year": "2023"},
        ),
        RetrievedDoc(
            id="doc2",
            content="Bức xạ mặt trời tại Hà Nội trung bình 3.8 kWh/m²/ngày.",
            score=0.85,
            metadata={"title": "Bản đồ bức xạ mặt trời Việt Nam", "year": "2022"},
        ),
    ]


@pytest.fixture
def mock_pipeline(mock_docs):
    """RAGPipeline với retriever và generator đã được mock."""
    from src.core.config import get_settings  # noqa: PLC0415

    settings = get_settings()
    mock_retriever = AsyncMock()
    mock_retriever.retrieve.return_value = mock_docs
    mock_retriever.close = AsyncMock()

    mock_generator = AsyncMock()
    mock_generator.generate.return_value = "Hệ thống 5 kWp phù hợp, dựa trên [1][2]."

    return RAGPipeline(settings, mock_retriever, mock_generator)


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestRAGPipeline:
    @pytest.mark.asyncio
    async def test_run_returns_pipeline_result(self, mock_pipeline):
        result = await mock_pipeline.run("Tôi cần hệ thống bao nhiêu kWp?")
        assert isinstance(result, PipelineResult)

    @pytest.mark.asyncio
    async def test_run_calls_retrieve(self, mock_pipeline, mock_docs):
        await mock_pipeline.run("câu hỏi test")
        mock_pipeline.retriever.retrieve.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_run_calls_generate_with_docs(self, mock_pipeline, mock_docs):
        await mock_pipeline.run("câu hỏi test")
        call_args = mock_pipeline.generator.generate.call_args
        # Docs được truyền vào generator
        assert call_args[0][1] == mock_docs

    @pytest.mark.asyncio
    async def test_citations_populated(self, mock_pipeline, mock_docs):
        result = await mock_pipeline.run("câu hỏi test")
        assert len(result.citations) == len(mock_docs)
        assert result.citations[0]["title"] == mock_docs[0].title

    @pytest.mark.asyncio
    async def test_run_with_history(self, mock_pipeline):
        history = [
            {"role": "user", "content": "Xin chào"},
            {"role": "assistant", "content": "Xin chào bạn!"},
        ]
        result = await mock_pipeline.run("câu hỏi tiếp theo", history=history)
        assert result.answer  # Không rỗng

    @pytest.mark.asyncio
    async def test_close_calls_retriever_close(self, mock_pipeline):
        await mock_pipeline.close()
        mock_pipeline.retriever.close.assert_awaited_once()


class TestRetrievedDoc:
    def test_properties(self, mock_docs):
        doc = mock_docs[0]
        assert doc.title == "Hướng dẫn lắp điện mặt trời"
        assert doc.source == "EVN"
        assert doc.year == "2023"

    def test_missing_metadata_defaults(self):
        doc = RetrievedDoc(id="x", content="test", score=0.5)
        assert doc.title == "Không rõ tiêu đề"
        assert doc.source == ""
        assert doc.year == ""
