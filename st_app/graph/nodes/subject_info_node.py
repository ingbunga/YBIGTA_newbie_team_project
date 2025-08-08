from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


def subject_info_node(state: Dict) -> Dict:
    query: str = state["input"].lower()
    db = json.loads(Path("st_app/db/subject_information/subjects.json").read_text(encoding="utf-8"))
    # 매우 단순한 매칭: 이름이 포함되면 해당 요약/스펙을 반환
    for item in db:
        if item["name"].lower() in query or item["id"].lower() in query:
            spec = item.get("spec", {})
            spec_str = ", ".join(f"{k}: {v}" for k, v in spec.items()) if spec else "정보 없음"
            msg = f"[{item['name']}] 요약: {item.get('summary','없음')}\n스펙: {spec_str}"
            return {"output": msg}
    return {"output": "대상 정보를 찾지 못했습니다."}


