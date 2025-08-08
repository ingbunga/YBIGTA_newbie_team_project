from __future__ import annotations

import os
from typing import Optional

from langchain.chat_models.openai import ChatOpenAI


def get_llm(model: str = "gpt-4o-mini", temperature: float = 0.2) -> ChatOpenAI:
    api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # 로컬 개발 편의를 위해 dummy 키 허용 처리 (실 운용에서는 필수)
        raise RuntimeError("OPENAI_API_KEY 환경변수가 필요합니다.")
    return ChatOpenAI(model=model, temperature=temperature, api_key=api_key)


