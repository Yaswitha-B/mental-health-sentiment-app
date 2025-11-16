import streamlit as st
from model_loader import load_all_models
from detection import initialize_models
from chat_ui import chat_ui

st.set_page_config(page_title="Mental Health Chat Helper", layout="wide")

models = load_all_models()
initialize_models(models)

st.title("Mental Health Chat Helper")
chat_ui()
