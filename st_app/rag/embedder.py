from __future__ import annotations

from typing import List

from sentence_transformers import SentenceTransformer


_MODEL_CACHE: dict[str, SentenceTransformer] = {}


def get_embedder(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> SentenceTransformer:
    if model_name not in _MODEL_CACHE:
        _MODEL_CACHE[model_name] = SentenceTransformer(model_name)
    return _MODEL_CACHE[model_name]


def encode_texts(texts: List[str]) -> List[List[float]]:
    model = get_embedder()
    return model.encode(texts, normalize_embeddings=True).tolist()


