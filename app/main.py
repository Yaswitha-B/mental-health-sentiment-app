import streamlit as st
from model_loader import load_all_models
from chat_tab import chat_tab
from analyse_tab import analyse_tab
from guide_tab import guide_tab

st.set_page_config(page_title="Mental Health Chat Helper", layout="wide")

# Load models once at startup (cached - only runs once)
models = load_all_models()

st.title("Mental Health Chat Helper")
st.sidebar.title("🧭 Navigation")
selected_tab = st.sidebar.radio("Go to:", ["💬 Chat", "📊 Analyse", "📖 Guide"], index=0)

if selected_tab == "💬 Chat":
    chat_tab()
elif selected_tab == "📊 Analyse":
    analyse_tab()
elif selected_tab == "📖 Guide":
    guide_tab()
