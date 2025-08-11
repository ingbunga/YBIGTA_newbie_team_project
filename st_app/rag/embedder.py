from __future__ import annotations

import os
from typing import List

from langchain_upstage import UpstageEmbeddings
from pydantic import SecretStr
import streamlit as st


_MODEL_CACHE: dict[str, UpstageEmbeddings] = {}
api_key = SecretStr(os.getenv("UPSTAGE_API_KEY") or st.secrets.get("UPSTAGE_API_KEY", ""))

def get_embedder(model_name: str = "solar-embedding-1-large") -> UpstageEmbeddings:
    if not api_key:
        raise RuntimeError("UPSTAGE_API_KEY 환경변수가 필요합니다.")
    if model_name not in _MODEL_CACHE:
        _MODEL_CACHE[model_name] = UpstageEmbeddings(model=model_name, api_key=api_key)
    return _MODEL_CACHE[model_name]


def encode_texts(texts: List[str]) -> List[List[float]]:
    embedder = get_embedder()
    vectors = embedder.embed_documents(texts)
    return vectors


