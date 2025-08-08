from __future__ import annotations

from typing import TypedDict


class ConversationState(TypedDict, total=False):
    input: str
    output: str


