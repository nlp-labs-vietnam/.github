"""
modules/embedding/embedding.py
────────────────────────────────
Chuyển văn bản tiếng Việt thành dense vector embeddings dùng cho RAG.
Hỗ trợ 2 backend:
  1. sentence-transformers  (chất lượng cao, dùng cho production)
  2. mock                   (dùng cho testing, không cần GPU)

Ví dụ sử dụng:
    embedder = VietnameseEmbedder({"model_name": "keepitreal/vietnamese-sbert"})
    vectors = embedder.embed(["Điện mặt trời 5 kWp", "Inverter Growatt"])
    # → numpy array shape (2, 768)
"""

from __future__ import annotations

import logging
import math
from pathlib import Path
from typing import Sequence

import numpy as np

logger = logging.getLogger(__name__)

# Model mặc định tối ưu cho tiếng Việt
DEFAULT_MODEL = "keepitreal/vietnamese-sbert"

# Kích thước vector của các model phổ biến
DIMENSION_MAP = {
    "keepitreal/vietnamese-sbert": 768,
    "VoVanPhuc/sup-SimCSE-Viet-roberta-base": 768,
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2": 384,
}


class VietnameseEmbedder:
    """
    Tạo embedding vectors cho văn bản tiếng Việt.

    Args:
        config: Dict cấu hình. Các key quan trọng:
            - model_name: tên model trên HuggingFace Hub
            - device: "cpu" | "cuda" | "auto"
            - batch_size: số lượng câu xử lý một lần
            - normalize: bool — chuẩn hóa L2 (mặc định True)
    """

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or {}
        self.model_name: str = self.config.get("model_name", DEFAULT_MODEL)
        self.device: str = self.config.get("device", "cpu")
        self.batch_size: int = self.config.get("batch_size", 32)
        self.normalize: bool = self.config.get("normalize", True)
        self.dimension: int = DIMENSION_MAP.get(self.model_name, 768)
        self._model = self._load_model()

    def _load_model(self):
        """Nạp SentenceTransformer model, fallback sang mock nếu không có."""
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Đang nạp model: %s", self.model_name)
            model = SentenceTransformer(self.model_name, device=self.device)
            self.dimension = model.get_sentence_embedding_dimension()
            logger.info("Model loaded — dim=%d device=%s", self.dimension, self.device)
            return model
        except ImportError:
            logger.warning("sentence-transformers không có — dùng mock embedder")
            return None

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        """
        Tạo embedding cho danh sách văn bản.

        Args:
            texts: Danh sách chuỗi văn bản.

        Returns:
            numpy array shape (len(texts), dimension).
        """
        if not texts:
            return np.empty((0, self.dimension), dtype=np.float32)

        if self._model is None:
            return self._mock_embed(texts)

        vectors = self._model.encode(
            list(texts),
            batch_size=self.batch_size,
            normalize_embeddings=self.normalize,
            show_progress_bar=len(texts) > 100,
        )
        return vectors.astype(np.float32)

    def embed_one(self, text: str) -> np.ndarray:
        """Tạo embedding cho một câu duy nhất — shape (dimension,)."""
        return self.embed([text])[0]

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Tính độ tương đồng cosine giữa 2 vectors."""
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def _mock_embed(self, texts: Sequence[str]) -> np.ndarray:
        """Mock embedding dùng cho testing — deterministic dựa trên hash."""
        rng = np.random.default_rng(seed=42)
        vectors = rng.standard_normal((len(texts), self.dimension)).astype(np.float32)
        if self.normalize:
            norms = np.linalg.norm(vectors, axis=1, keepdims=True)
            vectors = vectors / np.where(norms > 0, norms, 1)
        return vectors

    def process_batch(self, input_path: str) -> dict:
        """Entry point cho pipeline runner."""
        if not input_path or not Path(input_path).exists():
            return {"embedded": 0, "dimension": self.dimension}

        with open(input_path, encoding="utf-8") as f:
            texts = [line.strip() for line in f if line.strip()]

        vectors = self.embed(texts)
        return {
            "embedded": len(texts),
            "dimension": self.dimension,
            "shape": list(vectors.shape),
        }
