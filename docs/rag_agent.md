# RAG Agency

## 개요

이 프로젝트는 영화 리뷰 기반 RAG(Retrieval-Augmented Generation) 시스템을 구현하며, 대화 맥락을 유지하는 메모리 관리 기능을 포함합니다.

## 핵심 설계 원칙

### 1. State 기반 메모리 관리

기존의 대화 내역을 직접 매개변수로 넘기는 방식 대신, **State 객체**를 통한 통합적인 상태 관리를 구현했습니다.

```python
class ConversationState(TypedDict, total=False):
    input: str
    output: str
    next_node: str
    history: List[Message]  # 대화 히스토리
```

**장점:**
- 후에 툴 콜이나 다양한 기능 추가 시에도 수월함
- 툴, 챗 등 여러 가지를 개별적으로 넘기는 것은 복잡하지만, State 클래스에 저장해두면 접근 시 편리함
- 일관된 인터페이스로 모든 노드에서 동일한 방식으로 상태 접근 가능

### 2. 모듈화된 프롬프트 시스템

각 노드별로 전용 프롬프트 빌더를 모듈화하여 재사용성과 유지보수성을 높였습니다.


```python
# st_app/rag/prompt.py

def build_chat_prompt(user_input: str, state: dict) -> str:
    """기본 채팅 노드용 프롬프트"""
    # state에서 대화 히스토리 추출하여 맥락 유지
    history_text = ""
    if state and "history" in state:
        history = state["history"][-10:]  # 최근 10개 메시지 (5턴)
        if history:
            history_items = []
            for msg in history:
                role = "사용자" if msg["role"] == "user" else "AI"
                history_items.append(f"{role}: {msg['content']}")
            history_text = f"\n[대화 히스토리]\n" + "\n".join(history_items) + "\n"

def build_rag_prompt(query: str, contexts: list[str]) -> str:
    """RAG 리뷰 노드용 프롬프트"""
    joined = "\n- " + "\n- ".join(contexts) if contexts else ""
    return (
        f"[지시] 다음 사용자 질문에 대해 컨텍스트만 근거로 답하세요.\n"
        f"[질문] {query}\n"
        f"[컨텍스트]{joined}\n"
    )

def build_subject_info_prompt(query: str, items: list[dict]) -> str:
    """영화 정보 노드용 프롬프트"""
    # 구조화된 영화 정보를 프롬프트에 포함
    lines = []
    for it in items:
        spec = it.get("spec", {}) or {}
        spec_str = ", ".join(f"{k}: {v}" for k, v in spec.items()) if spec else "정보 없음"
        lines.append(
            f"- 이름: {it.get('name','?')} | 요약: {it.get('summary','정보 없음')} | 스펙: {spec_str}"
        )
    catalog = "\n".join(lines)
```


## 아키텍처

  

### LangGraph 기반 RAG 워크플로우

```
                    START
                      │
                      ▼
               ┌─────────────┐
               │ Chat Node   │ ◄── 중앙 라우터 및 응답 생성기
               │             │
               │ 1. LLM 라우팅 │    
               │ 2. 응답 생성  │    
               └──────┬──────┘
                      │
              ┌───────┼───────┐
              │       │       │
             ▼        ▼       ▼
      ┌─────────┐ ┌─────────┐ ┌─────────────┐
      │  Chat   │ │   RAG   │ │Subject Info │
      │         │ │ Review  │ │    Node     │
      │ 일반대화  │ │  Node   │ │             │
      │ 처리    │ │         │ │ 영화정보검색  │
      └────┬────┘ └────┬────┘ └─────┬───────┘
           │           │            │
           │    ┌──────▼──────┐     │
           │    │ FAISS 검색   │     │
           │    │ (리뷰 벡터)   │     │
           │    └─────────────┘     │
           │                       │
           │    ┌──────────────────▼┐
           │    │ subjects.json 검색 │
           │    │ (영화 기본정보)     │
           │    └───────────────────┘
           │                       │
           └───────────┬───────────┘
                       ▼
                      END
```



###  데이터 플로우

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 웹 크롤링     │ -> │ 전처리        │ -> │ 벡터화       │
│ (3개 사이트)  │    │ (텍스트 정제)  │    │ (Upstage)   │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 사용자 질의    │ -> │ 임베딩 검색    │ -> │ LLM 생성    │
│ (Streamlit) │    │ (FAISS)     │    │ (Upstage)   │
└─────────────┘    └─────────────┘    └─────────────┘
```




### 메모리 흐름
1. 사용자 입력 → State에 저장
2. Chat Node에서 라우팅 결정 → 전용 노드로 이동
3. LLM 응답 → State 업데이트 (출력 및 히스토리에 추가)
4. 다음 대화에서 누적된 히스토리 활용
