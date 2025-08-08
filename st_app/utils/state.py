from __future__ import annotations

from typing import TypedDict


class ConversationState(TypedDict, total=False):
    input: str
    output: str
    next_node: str  # 라우터에서 결정된 다음 노드


