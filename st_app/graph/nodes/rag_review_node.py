from __future__ import annotations

from typing import Dict

from ...rag.llm import get_llm
from ...rag.prompt import SYSTEM_RAG, build_rag_prompt
from ...rag.retriever import retrieve


def rag_review_node(state: Dict) -> Dict:
    print("=== RAG_REVIEW_NODE DEBUG ===")
    print(f"전체 state: {state}")
    print(f"state keys: {list(state.keys())}")

    query: str = state["input"]
    print(f"검색 쿼리: '{query}'")

    # 리뷰 검색
    print("리뷰 검색 시작...")
    retrieve_results = retrieve(query, k=4)
    print(f"검색 결과 수: {len(retrieve_results)}")

    contexts = [t for t, _ in retrieve_results]
    print("=== 검색된 리뷰 컨텍스트 ===")
    for i, context in enumerate(contexts):
        print(f"컨텍스트 {i+1}: {context[:100]}...")
    print("=== 컨텍스트 끝 ===")

    llm = get_llm()
    prompt = build_rag_prompt(query, contexts)

    history: list = state.get("history", [])
    msgs = [{"role": "system", "content": prompt}] + history
    print("=== RAG 프롬프트 ===")
    print(msgs)
    print("=== RAG 프롬프트 끝 ===")

    print("LLM 호출 중...")
    resp = llm.invoke(msgs)
    print(f"LLM 응답: {resp.content}")
    print("=== RAG DEBUG END ===\n")

    return {"output": resp.content, "history": history}
