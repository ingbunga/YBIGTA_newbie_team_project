from __future__ import annotations

SYSTEM_RAG = (
    "당신은 영화 리뷰 요약/참조를 도와주는 조수입니다. 주어진 컨텍스트만을 근거로 한국어로 간결히 답하세요."
)


def build_rag_prompt(query: str, contexts: list[str]) -> str:
    joined = "\n- " + "\n- ".join(contexts) if contexts else ""
    return (
        f"[지시] 다음 사용자 질문에 대해 컨텍스트만 근거로 답하세요. 필요 시 참고 문장을 인용하세요.\n"
        f"[질문] {query}\n"
        f"[컨텍스트]{joined}\n"
    )


