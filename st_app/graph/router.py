from __future__ import annotations

from typing import Dict

from langgraph.graph import END, StateGraph

from .nodes.chat_node import chat_node
from .nodes.subject_info_node import subject_info_node
from .nodes.rag_review_node import rag_review_node
from ..utils.state import ConversationState
from ..rag.llm import get_llm


SYSTEM_DECIDER = (
    "당신은 라우팅 분류기입니다. 사용자의 입력을 분석하여 어떤 노드로 라우팅할지 결정하세요:\n\n"
    "- chat: 일반적인 대화, 인사, 잡담 등 특별한 정보가 필요하지 않은 경우\n"
    "- subject_info: 영화나 제품의 기본 정보, 스펙, 감독, 배우 등에 대한 문의\n"  
    "- rag_review: 리뷰 내용, 평점, 관객 반응, 리뷰 요약/분석에 대한 문의\n\n"
    "반드시 다음 중 하나만 출력하세요: chat, subject_info, rag_review\n"
    "다른 텍스트나 설명은 포함하지 마세요."
)


def _decide_route(state: Dict) -> str:
    """LLM을 사용한 지능형 라우팅 결정"""
    user_text: str = state["input"]
    
    try:
        llm = get_llm(temperature=0.0)
        msgs = [
            {"role": "system", "content": SYSTEM_DECIDER},
            {"role": "user", "content": f"사용자 입력: {user_text}"},
        ]
        response = llm.invoke(msgs).content.strip().lower()
        
        # 유효한 라우트인지 확인
        if response in {"chat", "subject_info", "rag_review"}:
            return response
            
    except Exception as e:
        print(f"라우팅 결정 중 오류: {e}")
    
    # 폴백: 키워드 기반 라우팅
    text = user_text.lower()
    
    # Subject info 키워드들
    subject_keywords = ["정보", "스펙", "감독", "배우", "언제", "누가", "어떤", "기본", "상세"]
    if any(keyword in text for keyword in subject_keywords):
        return "subject_info"
    
    # RAG review 키워드들  
    review_keywords = ["리뷰", "평점", "평가", "반응", "어때", "좋아", "싫어", "추천", "요약", "분석"]
    if any(keyword in text for keyword in review_keywords):
        return "rag_review"
    
    # 기본값은 chat
    return "chat"


def router_node(state: Dict) -> Dict:
    """라우터 노드: 사용자 입력을 분석하여 다음 노드를 결정"""
    route = _decide_route(state)
    return {"next_node": route}


def should_continue(state: Dict) -> str:
    """라우터에서 결정된 다음 노드로 이동"""
    return state.get("next_node", "chat")


def build_graph() -> StateGraph:
    """개선된 LangGraph 구조"""
    graph = StateGraph(ConversationState)
    
    # 노드들 추가
    graph.add_node("router", router_node)
    graph.add_node("chat", chat_node)  
    graph.add_node("subject_info", subject_info_node)
    graph.add_node("rag_review", rag_review_node)
    
    # 라우터를 진입점으로 설정
    graph.set_entry_point("router")
    
    # 라우터에서 각 노드로의 조건부 라우팅
    graph.add_conditional_edges(
        "router",
        should_continue,
        {
            "chat": "chat",
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


