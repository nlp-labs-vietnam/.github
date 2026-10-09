"""
modules/embedding/tests/test_embedding.py
──────────────────────────────────────────
Unit tests cho VietnameseEmbedder.
Chạy: pytest modules/embedding/tests/ -v
"""

import numpy as np
import pytest
from modules.embedding.embedding import DEFAULT_MODEL, VietnameseEmbedder


@pytest.fixture
def mock_embedder():
    """Embedder dùng mock backend — không cần model download."""
    return VietnameseEmbedder({"model_name": DEFAULT_MODEL, "device": "cpu"})


@pytest.fixture
def solar_sentences():
    return [
        "Hệ thống điện mặt trời 5 kWp phù hợp cho hộ gia đình",
        "Inverter Growatt 5kW single phase giá tốt",
        "Quy hoạch Điện VIII mục tiêu 50% năng lượng tái tạo vào 2030",
    ]


class TestVietnameseEmbedder:
    def test_embed_returns_numpy_array(self, mock_embedder, solar_sentences):
        vectors = mock_embedder.embed(solar_sentences)
        assert isinstance(vectors, np.ndarray)

    def test_embed_shape(self, mock_embedder, solar_sentences):
        vectors = mock_embedder.embed(solar_sentences)
        assert vectors.shape == (len(solar_sentences), mock_embedder.dimension)

    def test_embed_empty_input(self, mock_embedder):
        vectors = mock_embedder.embed([])
        assert vectors.shape == (0, mock_embedder.dimension)

    def test_embed_one_shape(self, mock_embedder):
        vector = mock_embedder.embed_one("Điện mặt trời")
        assert vector.shape == (mock_embedder.dimension,)

    def test_embed_dtype_float32(self, mock_embedder, solar_sentences):
        vectors = mock_embedder.embed(solar_sentences)
        assert vectors.dtype == np.float32

    def test_cosine_similarity_identical(self, mock_embedder):
        v = mock_embedder.embed_one("test")
        sim = mock_embedder.cosine_similarity(v, v)
        assert abs(sim - 1.0) < 1e-5

    def test_cosine_similarity_range(self, mock_embedder, solar_sentences):
        v1 = mock_embedder.embed_one(solar_sentences[0])
        v2 = mock_embedder.embed_one(solar_sentences[1])
        sim = mock_embedder.cosine_similarity(v1, v2)
        assert -1.0 <= sim <= 1.0

    def test_cosine_similarity_zero_vector(self, mock_embedder):
        zero = np.zeros(mock_embedder.dimension, dtype=np.float32)
        v = mock_embedder.embed_one("test")
        sim = mock_embedder.cosine_similarity(zero, v)
        assert sim == 0.0

    def test_process_batch_nonexistent(self, mock_embedder):
        result = mock_embedder.process_batch("/no/such/file.txt")
        assert result["embedded"] == 0
        assert result["dimension"] == mock_embedder.dimension
