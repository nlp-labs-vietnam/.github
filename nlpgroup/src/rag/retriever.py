"""
src/rag/retriever.py
─────────────────────
Truy xuất tài liệu liên quan từ ChromaDB vector store.
Hỗ trợ dense search, hybrid search (dense + BM25), và reranking.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import chromadb
from chromadb import Collection

from src.core.config import Settings

logger = logging.getLogger(__name__)


@dataclass
class RetrievedDoc:
    """Tài liệu được truy xuất từ vector store."""
    id: str
    content: str
    score: float
    metadata: dict = field(default_factory=dict)

    @property
    def title(self) -> str:
        return self.metadata.get("title", "Không rõ tiêu đề")

    @property
    def source(self) -> str:
        return self.metadata.get("source", "")

    @property
    def year(self) -> str:
        return str(self.metadata.get("year", ""))

    @property
    def page(self) -> str:
        return str(self.metadata.get("page", ""))


class Retriever:
    """
    Truy xuất tài liệu từ ChromaDB.

    Args:
        settings: App settings.
        embedder: Module embedding đã khởi tạo (từ nlp-labs-cl).
    """

    def __init__(self, settings: Settings, embedder) -> None:
        self.settings = settings
        self.embedder = embedder
        self._client: chromadb.AsyncHttpClient | None = None
        self._collection: Collection | None = None

    @classmethod
    async def create(cls, settings: Settings, embedder) -> "Retriever":
        """Factory method — khởi tạo async connection tới ChromaDB."""
        instance = cls(settings, embedder)
        instance._client = await chromadb.AsyncHttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
        )
        instance._collection = await instance._client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            "Retriever sẵn sàng — collection=%s host=%s:%d",
            settings.CHROMA_COLLECTION, settings.CHROMA_HOST, settings.CHROMA_PORT,
        )
        return instance

    async def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievedDoc]:
        """
        Truy xuất top-k tài liệu phù hợp nhất với query.

        Args:
            query: Câu hỏi tiếng Việt của người dùng.
            top_k: Số lượng tài liệu cần lấy (mặc định từ settings).

        Returns:
            Danh sách RetrievedDoc đã sắp xếp theo điểm similarity giảm dần.
        """
        k = top_k or self.settings.RAG_TOP_K

        # Tạo embedding cho query
        query_vector = self.embedder.embed_one(query).tolist()

        if self._collection is None:
            logger.warning("Collection chưa được khởi tạo — trả về rỗng")
            return []

        results = await self._collection.query(
            query_embeddings=[query_vector],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

        docs = []
        for doc_id, content, metadata, distance in zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            # ChromaDB cosine distance: score = 1 - distance
            score = 1.0 - distance
            if score < self.settings.RAG_SIMILARITY_THRESHOLD:
                continue
            docs.append(RetrievedDoc(
                id=doc_id,
                content=content,
                score=round(score, 4),
                metadata=metadata or {},
            ))

        logger.debug("retrieve: query=%r top_k=%d returned=%d", query[:50], k, len(docs))
        return docs

    async def close(self) -> None:
        """Giải phóng kết nối."""
        if self._client:
            # chromadb async client không cần close tường minh
            self._client = None
