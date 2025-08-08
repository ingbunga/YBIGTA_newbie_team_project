from __future__ import annotations

from typing import Dict

from ...rag.llm import get_llm


def chat_node(state: Dict) -> Dict:
    llm = get_llm()
    user_input = state["input"]
    resp = llm.invoke([{"role": "user", "content": user_input}])
    return {"output": resp.content}


