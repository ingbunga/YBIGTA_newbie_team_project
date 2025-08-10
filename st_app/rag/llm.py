from __future__ import annotations

import os
from typing import Optional
from pydantic import SecretStr
from langchain_upstage import ChatUpstage

api_key = SecretStr(os.getenv("UPSTAGE_API_KEY", ''))

def get_llm(model: str = "solar-pro-250422", temperature: float = 0.2) -> ChatUpstage:
    if not api_key:
        raise RuntimeError("UPSTAGE_API_KEY 환경변수가 필요합니다.")
    return ChatUpstage(model=model, temperature=temperature, api_key=api_key)


