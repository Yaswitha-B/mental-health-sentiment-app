import streamlit as st

def analyse_tab():
    st.header("🔎 Analyse")
    st.info("This tab will analyse your latest message and detect your emotion.")
    st.button("Analyse", key="analyse_btn")
    st.write("Emotion: _Not analysed yet_")