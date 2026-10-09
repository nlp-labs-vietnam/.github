"""
modules/tokenizer/tokenizer.py
───────────────────────────────
Tokenizer tiếng Việt — hỗ trợ 3 backend:
  1. underthesea  (mặc định, tốt nhất cho tiếng Việt)
  2. pyvi         (nhẹ hơn, dùng cho inference real-time)
  3. whitespace   (fallback đơn giản, dùng cho testing)

Ví dụ sử dụng:
    tokenizer = VietnameseTokenizer({"backend": "underthesea"})
    tokens = tokenizer.tokenize("Hệ thống điện mặt trời 5 kWp tại Hà Nội")
    # → ["Hệ thống", "điện", "mặt trời", "5", "kWp", "tại", "Hà Nội"]
"""

from __future__ import annotations

import logging
from enum import Enum
from pathlib import Path
from typing import Iterator

logger = logging.getLogger(__name__)


class TokenizerBackend(str, Enum):
    UNDERTHESEA = "underthesea"
    PYVI = "pyvi"
    WHITESPACE = "whitespace"


class VietnameseTokenizer:
    """
    Tokenizer đa backend cho tiếng Việt.

    Args:
        config: Dict cấu hình. Các key quan trọng:
            - backend: "underthesea" | "pyvi" | "whitespace"
            - keep_punctuation: bool (mặc định True)
            - lowercase: bool (mặc định False)
    """

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or {}
        self.backend = TokenizerBackend(self.config.get("backend", "underthesea"))
        self.keep_punctuation: bool = self.config.get("keep_punctuation", True)
        self.lowercase: bool = self.config.get("lowercase", False)
        self._backend_fn = self._load_backend()

    def _load_backend(self):
        """Nạp backend tokenizer, fallback sang whitespace nếu không có."""
        if self.backend == TokenizerBackend.UNDERTHESEA:
            try:
                from underthesea import word_tokenize
                logger.info("Backend: underthesea")
                return word_tokenize
            except ImportError:
                logger.warning("underthesea không có — fallback sang whitespace")
                self.backend = TokenizerBackend.WHITESPACE

        if self.backend == TokenizerBackend.PYVI:
            try:
                from pyvi import ViTokenizer
                logger.info("Backend: pyvi")
                return ViTokenizer.tokenize
            except ImportError:
                logger.warning("pyvi không có — fallback sang whitespace")
                self.backend = TokenizerBackend.WHITESPACE

        logger.info("Backend: whitespace")
        return lambda text: text.split()

    def tokenize(self, text: str) -> list[str]:
        """
        Phân tách từ cho một chuỗi văn bản.

        Args:
            text: Văn bản tiếng Việt cần tokenize.

        Returns:
            Danh sách các token.
        """
        if not text or not text.strip():
            return []

        if self.lowercase:
            text = text.lower()

        tokens = self._backend_fn(text)

        if isinstance(tokens, str):
            # pyvi trả về string với dấu gạch dưới
            tokens = tokens.replace("_", " ").split()

        if not self.keep_punctuation:
            tokens = [t for t in tokens if t.isalnum() or "_" in t]

        return tokens

    def tokenize_batch(self, texts: list[str]) -> list[list[str]]:
        """Tokenize một batch văn bản."""
        return [self.tokenize(t) for t in texts]

    def tokenize_file(self, path: str | Path) -> Iterator[list[str]]:
        """Generator: tokenize từng dòng trong file."""
        path = Path(path)
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield self.tokenize(line)

    def process_batch(self, input_path: str) -> dict:
        """Entry point cho pipeline: đọc file, tokenize, trả về thống kê."""
        if not input_path or not Path(input_path).exists():
            return {"processed": 0, "tokens_total": 0}

        results = list(self.tokenize_file(input_path))
        total_tokens = sum(len(r) for r in results)
        return {
            "processed": len(results),
            "tokens_total": total_tokens,
            "avg_tokens_per_sentence": total_tokens / len(results) if results else 0,
        }
