import streamlit as st
import time
from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

if API_KEY is None:
    raise ValueError("OpenRouter API Key not found!")

def chat_tab():
    st.header("💬 Chat with MindMate")
    initialize_session()
    chat_ui()

def initialize_session():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
        st.session_state["chat_history"].append({"role": "assistant", "content": "Hello user! How are you feeling today?"})

    if "waiting_for_response" not in st.session_state:
        st.session_state["waiting_for_response"] = False

def chat_ui():
    # Chat display
    chat_display = ""
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            chat_display += f'<div style="text-align:right;margin:8px 0;"><div style="background:#007bff;color:white;padding:8px 12px;border-radius:15px;display:inline-block;max-width:70%;">👤 {msg["content"]}</div></div>'
        else:
            chat_display += f'<div style="text-align:left;margin:8px 0;"><div style="background:#f1f1f1;color:#333;padding:8px 12px;border-radius:15px;display:inline-block;max-width:70%;">🤖 {msg["content"]}</div></div>'
    
    st.markdown(f'<div style="height:400px;overflow-y:auto;padding:10px;background:#fafafa;border-radius:8px;" id="chat">{chat_display}</div>', unsafe_allow_html=True)
    
    # Auto-scroll script
    st.markdown('<script>setTimeout(()=>{const c=document.getElementById("chat");if(c)c.scrollTop=c.scrollHeight;},100);</script>', unsafe_allow_html=True)

    # Input
    user_input = st.text_input("Type and press Enter...", key="msg_input", on_change=handle_message, placeholder="Share what's on your mind...", disabled=st.session_state["waiting_for_response"], label_visibility="collapsed")

def handle_message():
    user_input = st.session_state["msg_input"]
    if user_input.strip():
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        st.session_state["waiting_for_response"] = True
        
        with st.spinner("Thinking..."):
            bot_response = get_bot_response()
        
        st.session_state["chat_history"].append({"role": "assistant", "content": bot_response})
        st.session_state["waiting_for_response"] = False
        st.session_state["msg_input"] = ""
        st.rerun()

def get_bot_response():
    try:
        raise Exception("API Key not found!")
        history = st.session_state["chat_history"]
        
        # Build context
        if len(history) > 1:
            prev_msgs = [f"{msg['role']}: {msg['content']}" for msg in history[-7:-1]]
            context = f"You are a psychologist trying to understand the user's emotions. Ask small questions and respond with small answers, be supportive, don't suggest any solutions for the problem yet. Previous context: {' | '.join(prev_msgs)}"
        else:
            context = "You are a psychologist trying to understand the user's emotions. Ask small questions, be supportive, don't suggest yet."
        
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": history[-1]["content"]}
        ]
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": "mistralai/mistral-7b-instruct", "messages": messages, "temperature": 0.7, "max_tokens": 150},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            return "I'm here to listen. How are you feeling right now?"
            
    except Exception as e:
        return "I want to understand what you're going through. Can you tell me more?"