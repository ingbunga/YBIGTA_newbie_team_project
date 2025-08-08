from __future__ import annotations

from typing import Dict

from ...rag.llm import get_llm
from ...rag.prompt import SYSTEM_RAG, build_rag_prompt
from ...rag.retriever import retrieve


def rag_review_node(state: Dict) -> Dict:
    query: str = state["input"]
    contexts = [t for t, _ in retrieve(query, k=4)]
    llm = get_llm()
    prompt = build_rag_prompt(query, contexts)
    msgs = [
        {"role": "system", "content": SYSTEM_RAG},
        {"role": "user", "content": prompt},
    ]
    resp = llm.invoke(msgs)
    return {"output": resp.content}


