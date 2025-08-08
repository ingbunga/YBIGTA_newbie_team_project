from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

import faiss  # type: ignore
import json

from .embedder import encode_texts


@dataclass
class IndexedDoc:
    text: str
    metadata: dict


@lru_cache(maxsize=1)
def _index_path() -> Path:
    return Path("st_app/db/faiss_index/index.faiss")


@lru_cache(maxsize=1)
def _meta_path() -> Path:
    return Path("st_app/db/faiss_index/meta.json")


def ensure_simple_index_from_datasets() -> None:
    """데모용 RAG 인덱스. 프로젝트의 `database/` 리뷰 CSV 일부를 묶어 인덱스 생성.

    - 실제 운영에서는 사전 전처리 후 임베딩/색인 과정을 별도 파이프라인으로 두어야 함
    """
    ipath = _index_path()
    mpath = _meta_path()
    if ipath.exists() and mpath.exists():
        return

    docs: List[IndexedDoc] = []
    # 간단히 네이버 리뷰에서 앞부분만 사용
    src = Path("database/reviews_naver.csv")
    if src.exists():
        lines = src.read_text(encoding="utf-8").splitlines()[1:300]
        for line in lines:
            parts = line.split(",", 3)
            if len(parts) == 4:
                rating, date, text = parts[1], parts[2], parts[3]
                docs.append(IndexedDoc(text=text, metadata={"source": "naver", "rating": rating, "date": date}))
    else:
        # fallback 문서
        docs = [
            IndexedDoc(text="이 영화는 스토리가 탄탄하고 연출이 뛰어나다", metadata={"source": "fallback"}),
            IndexedDoc(text="배우들의 연기가 훌륭해 감정 이입이 잘된다", metadata={"source": "fallback"}),
        ]

    texts = [d.text for d in docs]
    vectors = encode_texts(texts)
    dim = len(vectors[0])
    index = faiss.IndexFlatIP(dim)
    import numpy as np

    index.add(np.array(vectors, dtype="float32"))
    ipath.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(ipath))
    mpath.write_text(json.dumps({"documents": [d.__dict__ for d in docs]}, ensure_ascii=False), encoding="utf-8")


def retrieve(query: str, k: int = 3) -> List[Tuple[str, dict]]:
    ensure_simple_index_from_datasets()
    import numpy as np
    ipath, mpath = _index_path(), _meta_path()
    index = faiss.read_index(str(ipath))
    meta = json.loads(mpath.read_text(encoding="utf-8"))
    
    # Handle different meta.json formats
    if isinstance(meta, dict) and "documents" in meta:
        documents = meta["documents"]
        texts = [d["text"] for d in documents]
    else:
        # meta is a list directly
        documents = meta
        texts = [d["review"] for d in documents]  # Use "review" field from the actual structure
    
    qvec = encode_texts([query])[0]
    D, I = index.search(np.array([qvec], dtype="float32"), k)
    results: List[Tuple[str, dict]] = []
    for idx in I[0]:
        if idx == -1:
            continue
        doc = documents[int(idx)]
        if isinstance(meta, dict) and "documents" in meta:
            results.append((doc["text"], doc.get("metadata", {})))
        else:
            # Convert to expected format
            metadata = {k: v for k, v in doc.items() if k != "review"}
            results.append((doc["review"], metadata))
    return results


