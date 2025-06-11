import streamlit as st
from chat_tab import chat_tab
from analyse_tab import analyse_tab
from guide_tab import guide_tab

st.set_page_config(page_title="AI Mental Health Chat Helper", page_icon="🧠", layout="centered")
st.title("🧠 AI Mental Health Chat Helper")

selected_tab = st.sidebar("Navigate", ["Chat", "Analyse", "Guide"])

if selected_tab == "Chat":
    chat_tab()
elif selected_tab == "Analyse":
    analyse_tab()
elif selected_tab == "Guide":
    guide_tab()