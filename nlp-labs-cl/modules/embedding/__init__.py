"""
modules/embedding/__init__.py
Embedding module — Chuyển văn bản thành vector
"""

from .embedding import VietnameseEmbedder

__all__ = ["VietnameseEmbedder", "run"]


def run(config: dict) -> dict:
    """Entry point cho pipeline runner."""
    embedder = VietnameseEmbedder(config)
    return embedder.process_batch(config.get("input_path", ""))
