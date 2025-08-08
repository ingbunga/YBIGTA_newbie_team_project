from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from ...rag.prompt import (
    build_subject_info_prompt,
    SYSTEM_SUBJECT,
)
from ...rag.llm import get_llm


def subject_info_node(state: Dict) -> Dict:
    print("=== SUBJECT_INFO_NODE DEBUG ===")
    print(f"전체 state: {state}")
    print(f"state keys: {list(state.keys())}")

    query: str = state["input"].lower()
    print(f"검색 쿼리: '{state['input']}' (소문자: '{query}')")

    db = json.loads(
        Path("st_app/db/subject_information/subjects.json").read_text(encoding="utf-8")
    )
    print(f"DB에서 로드된 아이템 수: {len(db)}")

    print("주제 매칭 시작...")
    for item in db:
        print(
            f"매칭 체크: '{item['name'].lower()}' in '{query}' or '{item['id'].lower()}' in '{query}'"
        )
        if item["name"].lower() in query or item["id"].lower() in query:
            print(f"매칭 성공: {item['name']} ({item['id']})")
            # 매칭되면 해당 항목만을 주제목록으로 LLM 프롬프트 생성 후 응답
            llm = get_llm()
            prompt = build_subject_info_prompt(state["input"], [item])
            msgs = [
                {"role": "system", "content": SYSTEM_SUBJECT},
                {"role": "user", "content": prompt},
            ]
            resp = llm.invoke(msgs)
            print("=== SUBJECT LLM RESP (matched) ===")
            print(resp.content)
            print("=== SUBJECT DEBUG END ===\n")
            return {"output": resp.content}

    # 매칭이 없으면 LLM에 주제 목록과 함께 질의를 전달해 선택·응답하도록 위임
    llm = get_llm()
    prompt = build_subject_info_prompt(state["input"], db)
    msgs = [
        {"role": "system", "content": SYSTEM_SUBJECT},
        {"role": "user", "content": prompt},
    ]
    resp = llm.invoke(msgs)
    print("=== SUBJECT LLM RESP ===")
    print(resp.content)
    print("=== SUBJECT DEBUG END ===\n")
    return {"output": resp.content}
