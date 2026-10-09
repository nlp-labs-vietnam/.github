"""
src/rag/_mock_embedder.py
──────────────────────────
Mock embedder dùng khi nlp-labs-cl không có trong PATH.
Chỉ dùng trong testing và fallback — không dùng trong production.
"""

import numpy as np


class MockEmbedder:
    """Deterministic mock — trả về vector random seed=42."""
    dimension = 768

    def embed_one(self, text: str) -> np.ndarray:
        rng = np.random.default_rng(seed=abs(hash(text)) % (2**32))
        v = rng.standard_normal(self.dimension).astype(np.float32)
        return v / (np.linalg.norm(v) + 1e-9)

    def embed(self, texts):
        return np.stack([self.embed_one(t) for t in texts])
