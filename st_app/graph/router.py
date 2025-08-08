from __future__ import annotations

from typing import Dict

from langgraph.graph import END, StateGraph

from .nodes.chat_node import chat_node
from .nodes.subject_info_node import subject_info_node
from .nodes.rag_review_node import rag_review_node
from .route_decider_llm import decide_route_llm
from ..utils.state import ConversationState


def _decide_route(state: Dict) -> str:
    # LLM 기반 분류기로 규칙 기반 라우팅을 대체
    return decide_route_llm(state["input"])


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


