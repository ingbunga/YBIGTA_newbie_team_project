from __future__ import annotations

from typing import Dict

from langgraph.graph import END, StateGraph

from .nodes.chat_node import chat_node
from .nodes.subject_info_node import subject_info_node
from .nodes.rag_review_node import rag_review_node
from ..utils.state import ConversationState


def should_continue(state: Dict) -> str:
    """라우터에서 결정된 다음 노드로 이동"""
    return state.get("next_node", "chat")


def build_graph() -> StateGraph:
    """개선된 LangGraph 구조"""
    graph = StateGraph(ConversationState)
    
    # 노드들 추가
    graph.add_node("chat", chat_node)                   # type: ignore
    graph.add_node("subject_info", subject_info_node)   # type: ignore
    graph.add_node("rag_review", rag_review_node)       # type: ignore

    # 라우터를 진입점으로 설정
    graph.set_entry_point("chat")

    # 라우터에서 각 노드로의 조건부 라우팅
    graph.add_conditional_edges(
        "chat",
        should_continue,
        {
            "chat": END,
            "subject_info": "subject_info", 
            "rag_review": "rag_review",
        }
    )
    
    # 모든 노드 처리 후 END로 이동 (무한 루프 방지)
    graph.add_edge("chat", END)
    graph.add_edge("subject_info", END)  
    graph.add_edge("rag_review", END)
    
    return graph


_GRAPH = None


def get_or_create_graph():
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = build_graph().compile()
    return _GRAPH


