"""Zero-cost deterministic hashed token vectors for Phase 2.

This is intentionally provider-free for the POC foundation. The interface can later
be replaced by an API embedding provider without changing ProductMatcher.
"""
import hashlib
import re
import numpy as np

class EmbeddingService:
    def __init__(self, dimensions: int = 256):
        self.dimensions = dimensions

    def embed(self, text: str) -> np.ndarray:
        vector = np.zeros(self.dimensions, dtype=float)
        tokens = re.findall(r"[a-z0-9]+", text.lower().replace("_", " "))
        for token in tokens:
            digest = hashlib.sha256(token.encode()).digest()
            idx = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[idx] += 1.0
        norm = np.linalg.norm(vector)
        return vector / norm if norm else vector

    @staticmethod
    def similarity(a: np.ndarray, b: np.ndarray) -> float:
        if not np.any(a) or not np.any(b):
            return 0.0
        # normalized vectors: cosine [-1,1], but our count vectors are non-negative.
        return float(np.clip(np.dot(a, b), 0.0, 1.0))
