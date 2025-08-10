from __future__ import annotations

from typing import Dict
from langchain.tools import tool
from ...rag.llm import get_llm
from langchain_core.messages import AIMessage


SYSTEM_PROMPT = """당신은 영화 리뷰 분석 전문 AI 어시스턴트입니다.
사용자의 질문을 분석하여 적절한 도구를 사용하세요:
- 리뷰 검색이나 분석이 필요한 경우: **반드시** route_to_rag_review_node 도구를 사용해서 rag_review_node이 대신 답하게 하세요.
- 영화 정보나 기본 데이터가 필요한 경우: **반드시** route_to_subject_info_node 도구를 사용해서 subject_info_node이 대신 답하게 하세요.
- 일반적인 대화나 인사: 직접 응답 하세요.

항상 친절하고 도움이 되는 답변을 제공하세요."""
DEFAULT_ROUTING = 'chat'


def chat_node(state: Dict) -> Dict:
    route = DEFAULT_ROUTING

    @tool(parse_docstring=True)
    def route_to_rag_review_node() -> None:
        '''rag review 노드에게 대신 요청을 넘깁니다.'''
        nonlocal route
        route = "rag_review"

    @tool(parse_docstring=True)
    def route_to_subject_info_node() -> None:
        '''subject info 노드에게 대신 요청을 넘깁니다.'''
        nonlocal route
        route = "subject_info"

    tools = [route_to_rag_review_node, route_to_subject_info_node]
    llm = get_llm()
    llm_with_tools = llm.bind_tools(tools)

    history: list = state.get("history", [])
    messages = history[:-1] + [{"role": "system", "content": SYSTEM_PROMPT}] + history[-1:]
    resp: AIMessage = llm_with_tools.invoke(messages)   # type: ignore

    # 도구 호출이 있다면 실행
    toolname_func_map = {t.name: t for t in tools}
    for tool_call in resp.tool_calls:
        tool_func = toolname_func_map.get(tool_call.get("name"))
        if tool_func:
            tool_func.invoke({})

    if route == DEFAULT_ROUTING:
        return {"output": resp.content, "history": history, "next_node": route}
    else:
        print(f"라우팅 결정: {route}")
        return {"next_node": route, "history": history}