from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from st_app.rag.llm import get_llm


def subject_info_node(state: Dict) -> Dict:
    print("=== SUBJECT_INFO_NODE DEBUG ===")
    print(f"전체 state: {state}")
    print(f"state keys: {list(state.keys())}")
    
    query: str = state["input"].lower()
    print(f"입력 쿼리: '{state['input']}' (소문자: '{query}')")
    
    db = json.loads(
        Path("st_app/db/subject_information/subjects.json").read_text(encoding="utf-8")
    )
    print(f"DB에서 로드된 아이템 수: {len(db)}")

    # 매칭되는 주제 찾기
    for item in db:
        print(f"매칭 체크: '{item['name'].lower()}' in '{query}' or '{item['id'].lower()}' in '{query}'")
        if item["name"].lower() in query or item["id"].lower() in query:
            # 주제 정보를 state에 저장하여 다른 노드에서 활용할 수 있도록 함
            subject_info = {
                "id": item["id"],
                "name": item["name"],
                "type": item["type"],
                "spec": item.get("spec", {}),
                "summary": item.get("summary", ""),
            }

            print(f"매칭된 아이템: {item}")
            
            # LLM을 사용하여 자연스러운 답변 생성
            llm = get_llm()

            # 컨텍스트 정보 구성
            context = f"""
주제 정보:
- 이름: {item['name']}
- 타입: {item['type']}
- 요약: {item.get('summary', '정보 없음')}
- 상세 정보: {', '.join(f'{k}: {v}' for k, v in item.get('spec', {}).items())}
"""

            prompt = f"""
다음 주제 정보를 바탕으로 사용자 질문에 자연스럽게 답변해주세요.

{context}

사용자 질문: {state['input']}

현재 상태 정보 (디버깅용):
- 전체 state: {state}
- 사용 가능한 state keys: {list(state.keys())}

답변 가이드라인:
1. 친근하고 자연스러운 톤으로 답변
2. 질문에 적절한 수준의 정보 제공
3. 마크다운 포맷 사용 가능
4. 한국어로 답변
"""
            
            print("=== LLM 프롬프트 ===")
            print(prompt)
            print("=== LLM 프롬프트 끝 ===")

            response = llm.invoke(prompt).content
            print(f"LLM 응답: {response}")
            print("=== DEBUG END ===\n")

            return {
                "output": response,
                "subject_info": subject_info,  # 다른 노드에서 활용 가능
            }

    print("매칭되는 주제를 찾지 못함")
    print("=== DEBUG END ===\n")
    return {"output": "해당 주제에 대한 정보를 찾지 못했습니다."}
