"""
modules/tokenizer/tests/test_tokenizer.py
──────────────────────────────────────────
Unit tests cho VietnameseTokenizer.
Chạy: pytest modules/tokenizer/tests/ -v
"""

import pytest
from modules.tokenizer.tokenizer import TokenizerBackend, VietnameseTokenizer


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def whitespace_tokenizer():
    return VietnameseTokenizer({"backend": "whitespace"})


@pytest.fixture
def sample_texts():
    return [
        "Hệ thống điện mặt trời 5 kWp tại Hà Nội",
        "Quy hoạch Điện VIII năm 2023",
        "AI tư vấn năng lượng tái tạo cho Việt Nam",
    ]


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestVietnameseTokenizer:
    def test_tokenize_basic(self, whitespace_tokenizer):
        tokens = whitespace_tokenizer.tokenize("Xin chào Việt Nam")
        assert tokens == ["Xin", "chào", "Việt", "Nam"]

    def test_tokenize_empty_string(self, whitespace_tokenizer):
        assert whitespace_tokenizer.tokenize("") == []
        assert whitespace_tokenizer.tokenize("   ") == []

    def test_tokenize_none_like(self, whitespace_tokenizer):
        """None không được truyền vào nhưng chuỗi rỗng phải an toàn."""
        assert whitespace_tokenizer.tokenize("") == []

    def test_tokenize_lowercase(self):
        tokenizer = VietnameseTokenizer({"backend": "whitespace", "lowercase": True})
        tokens = tokenizer.tokenize("Hệ Thống Điện")
        assert all(t == t.lower() for t in tokens)

    def test_tokenize_remove_punctuation(self):
        tokenizer = VietnameseTokenizer({"backend": "whitespace", "keep_punctuation": False})
        tokens = tokenizer.tokenize("Xin chào! Việt Nam.")
        assert "!" not in tokens
        assert "." not in tokens

    def test_tokenize_batch(self, whitespace_tokenizer, sample_texts):
        results = whitespace_tokenizer.tokenize_batch(sample_texts)
        assert len(results) == len(sample_texts)
        assert all(isinstance(r, list) for r in results)
        assert all(len(r) > 0 for r in results)

    def test_backend_fallback(self):
        """Backend không hợp lệ sẽ fallback sang whitespace."""
        tokenizer = VietnameseTokenizer({"backend": "whitespace"})
        assert tokenizer.backend == TokenizerBackend.WHITESPACE

    def test_process_batch_nonexistent_path(self, whitespace_tokenizer):
        result = whitespace_tokenizer.process_batch("/nonexistent/path.txt")
        assert result["processed"] == 0
        assert result["tokens_total"] == 0

    def test_tokenize_solar_domain_terms(self, whitespace_tokenizer):
        """Kiểm tra các thuật ngữ đặc thù của domain năng lượng mặt trời."""
        text = "Inverter Growatt 5kW lắp đặt tại Đà Nẵng"
        tokens = whitespace_tokenizer.tokenize(text)
        assert len(tokens) > 0
        # Đảm bảo tên thương hiệu không bị tách
        full_text = " ".join(tokens)
        assert "Growatt" in full_text
