from __future__ import annotations

from typing import Dict

from langgraph.graph import END, StateGraph

from .nodes.chat_node import chat_node
from .nodes.subject_info_node import subject_info_node
from .nodes.rag_review_node import rag_review_node
from ..utils.state import ConversationState
from ..rag.llm import get_llm


SYSTEM_DECIDER = (
    "당신은 라우팅 분류기입니다. 사용자의 입력을 아래 레이블 중 하나로만 판단해 출력하세요:\n"
    "- chat: 일반 대화\n- subject_info: 대상 정보/스펙 문의\n- rag_review: 리뷰 내용 참고/요약/추출 문의\n"
    "반드시 소문자 레이블 하나만 출력하고 다른 텍스트는 포함하지 마세요."
)


def _decide_route(state: Dict) -> str:
    user_text: str = state["input"]
    try:
        llm = get_llm(temperature=0.0)
        msgs = [
            {"role": "system", "content": SYSTEM_DECIDER},
            {"role": "user", "content": user_text},
        ]
        out = llm.invoke(msgs).content.strip().lower()
        if out in {"chat", "subject_info", "rag_review"}:
            return out
    except Exception:
        pass
    # 폴백 키워드
    text = user_text.lower()
    if any(k in text for k in ["정보", "주제", "spec", "스펙"]):
        return "subject_info"
    if any(k in text for k in ["리뷰", "평", "요약"]):
        return "rag_review"
    return "chat"


def build_graph() -> StateGraph:
    graph = StateGraph(ConversationState)
    graph.add_node("chat", chat_node)
    graph.add_node("subject_info", subject_info_node)
    graph.add_node("rag_review", rag_review_node)

    def route(state: Dict) -> str:
        dest = _decide_route(state)
        return dest

    graph.set_entry_point("chat")
    graph.add_conditional_edges(
        "chat",
        route,
        {
            "subject_info": "subject_info",
            "rag_review": "rag_review",
            "chat": END,
        },
    )

    # 각 노드 처리 후 다시 chat으로 회귀
    graph.add_edge("subject_info", "chat")
    graph.add_edge("rag_review", "chat")

    return graph


_GRAPH = None


def get_or_create_graph():
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = build_graph().compile()
    return _GRAPH


