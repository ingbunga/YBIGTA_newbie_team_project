import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    st.set_page_config(page_title="RAG Agent Demo", page_icon="🤖", layout="wide")
    st.title("RAG Agent Demo (LangGraph · Streamlit)")
    st.caption(
        "기본 대화(Chat) · 대상 정보(Subject Info) · 리뷰 RAG(Review) 노드를 LangGraph로 조건부 라우팅"
    )

    st.sidebar.header("환경 설정")
    st.sidebar.info(
        "Upstage/OpenAI 등 LLM 키는 환경변수로 설정해주세요. 예: OPENAI_API_KEY"
    )

    st.session_state.setdefault("messages", [])

    # 간단한 데모용 입력 UI. 실제 그래프 실행은 st_app/graph/router.py에 위임합니다.
    from st_app.graph.router import get_or_create_graph

    graph = get_or_create_graph()

    user_input = st.chat_input("메시지를 입력하세요… 예: 리뷰 내용 알려줘, 아이폰 스펙 알려줘")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        for event in graph.stream({"input": user_input}, stream_mode="values"):
            last = event.get("output")
            if last:
                st.session_state["messages"].append({"role": "assistant", "content": last})

    for m in st.session_state["messages"]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])


if __name__ == "__main__":
    main()


