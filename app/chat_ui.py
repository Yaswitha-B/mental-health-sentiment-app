import streamlit as st
from decision_tree import ConversationState, process_message


def chat_ui():
    st.header("💬 Chat with MindMate")
    initialize_chat_session()
    display_chat()
    handle_user_input()


def initialize_chat_session():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
        st.session_state["chat_history"].append({
            "role": "assistant",
            "content": "Hello! I'm here to listen and support you. How are you feeling today?"
        })

    if "conversation_state" not in st.session_state:
        st.session_state["conversation_state"] = ConversationState()

    if "chat_locked" not in st.session_state:
        st.session_state["chat_locked"] = False


def display_chat():
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(msg["content"])


def handle_user_input():
    is_locked = st.session_state.get("chat_locked", False)

    if is_locked:
        st.warning("🚨 Chat is locked. Please reach out to the crisis resources provided above.")
    else:
        user_input = st.chat_input("Share what's on your mind...")
        if user_input:
            process_user_message(user_input)
            st.rerun()


def process_user_message(user_input):
    st.session_state["chat_history"].append({
        "role": "user",
        "content": user_input
    })

    state = st.session_state["conversation_state"]
    bot_response = process_message(user_input, state)

    if isinstance(bot_response, dict):
        response_text = bot_response.get("response", "")
        if bot_response.get("locked", False):
            st.session_state["chat_locked"] = True
    else:
        response_text = bot_response

    st.session_state["chat_history"].append({
        "role": "assistant",
        "content": response_text
    })
