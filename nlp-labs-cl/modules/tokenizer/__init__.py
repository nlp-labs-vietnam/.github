"""
modules/tokenizer/__init__.py
Tokenizer module — Phân tách từ tiếng Việt
"""

from .tokenizer import VietnameseTokenizer

__all__ = ["VietnameseTokenizer", "run"]


def run(config: dict) -> dict:
    """Entry point cho pipeline runner."""
    tokenizer = VietnameseTokenizer(config)
    return tokenizer.process_batch(config.get("input_path", ""))
