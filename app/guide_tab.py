import streamlit as st

def guide_tab():
    st.header("🧘 Healing Guide")
    st.info("Get personalized mental health recommendations based on your detected emotion.")
    st.write("Please analyse your emotion first in the Analyse tab.")

#TODO:
#Analyze the entire repo once, find cure.py in data. teh emotions are there in session state, check analyse tab to see how they are stored there. 
# From each emotion in sessionsate detected by analyse, randomly pick a cure from cure.py and display it here with good ui.
# repeat this process for atleats 10 to 15 cures in random order even if the emotions are less. 
# Always ensure same cure is not repeated twice or less.
#Finish the entire thing with good ui and clean coding principles liek ETC, DRY, ORTHOGNALITY, etc
# Finish this with good ui.
# if the emotions are not there at all, tell them to go back to analyse tab and analyse their emotions first.