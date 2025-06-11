import streamlit as st
from streamlit.components.v1 import html

def chat_tab():
    st.header("💬 Chat")
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    # Chat message display area
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                st.markdown(f'<div style="text-align:right;background:#e6f7ff;padding:8px 12px;border-radius:12px;margin:4px 0;max-width:70%;float:right;">👤 <b>You:</b> {msg["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="text-align:left;background:#f4f4f4;padding:8px 12px;border-radius:12px;margin:4px 0;max-width:70%;float:left;">🤖 <b>MindMate:</b> {msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown("<div style='clear:both'></div>", unsafe_allow_html=True)
    # Input area
    user_input = st.text_input("Type your message...", "", key="chat_input")
    col1, col2 = st.columns([4,1])
    with col2:
        send = st.button("Send", key="send_btn")
    if send and user_input.strip():
        st.session_state["chat_history"].append({"role": "user", "text": user_input})
        st.experimental_rerun()