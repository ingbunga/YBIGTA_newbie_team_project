from __future__ import annotations

SYSTEM_RAG = (
    "당신은 영화 리뷰 요약/참조를 도와주는 조수입니다. 주어진 컨텍스트만을 근거로 한국어로 간결히 답하세요."
)


def build_rag_prompt(query: str, contexts: list[str]) -> str:
    joined = "\n- " + "\n- ".join(contexts) if contexts else ""
    return (
        f"[지시] 다음 사용자 질문에 대해 컨텍스트만 근거로 답하세요.\n"
        f"[질문] {query}\n"
        f"[컨텍스트]{joined}\n"
    )

# Subject Info용 LLM 프롬프트와 시스템 메시지
SYSTEM_SUBJECT = (
    "당신은 주제(제품/작품 등) 정보 안내원입니다. 제공된 주제 목록만 근거로 한국어로 답하세요."
)


def build_subject_info_prompt(query: str, items: list[dict]) -> str:
    lines = []
    for it in items:
        spec = it.get("spec", {}) or {}
        spec_str = ", ".join(f"{k}: {v}" for k, v in spec.items()) if spec else "정보 없음"
        lines.append(
            f"- 이름: {it.get('name','?')} | ID: {it.get('id','?')} | 요약: {it.get('summary','정보 없음')} | 스펙: {spec_str}"
        )
    catalog = "\n".join(lines)
    return (
        f"[지시] 아래 주제 목록만을 근거로 질문에 답하세요. 해당 주제를 찾기 어려우면 가장 가까운 항목을 선택해 답하고, 불확실하면 후보를 제시하세요.\n"
        f"[질문] {query}\n"
        f"[주제목록]\n{catalog}\n"
    )

