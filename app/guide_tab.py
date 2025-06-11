import streamlit as st
import random
from data.cures import emotion_cures

def setup_guide_styles():
    st.markdown("""
        <style>
        .cure-card {
            padding: 1.5rem;
            border-radius: 15px;
            background: linear-gradient(145deg, #ffffff, #f0f0f0);
            box-shadow: 5px 5px 10px #d9d9d9, -5px -5px 10px #ffffff;
            margin: 15px 0;
            transition: transform 0.3s ease;
        }
        .cure-card:hover {
            transform: translateY(-5px);
        }
        .emotion-tag {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            background: #007bff;
            color: white;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .cure-text {
            font-size: 1.1em;
            color: #2c3e50;
            line-height: 1.6;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def render_cure_card(emotion, cure):
    return f"""
        <div class='cure-card'>
            <div class='emotion-tag'>{emotion.title()}</div>
            <div class='cure-text'>{cure}</div>
        </div>
    """

def get_random_cures(emotions, num_cures=15):
    all_cures = []
    used_cures = set()
    
    # First, get one cure for each detected emotion
    for emotion, _ in emotions:
        if emotion in emotion_cures:
            available_cures = [cure for cure in emotion_cures[emotion] if cure not in used_cures]
            if available_cures:
                cure = random.choice(available_cures)
                all_cures.append((emotion, cure))
                used_cures.add(cure)
    
    # Then fill up to num_cures with random cures from detected emotions
    while len(all_cures) < num_cures and emotions:
        emotion = random.choice([e for e, _ in emotions])
        if emotion in emotion_cures:
            available_cures = [cure for cure in emotion_cures[emotion] if cure not in used_cures]
            if available_cures:
                cure = random.choice(available_cures)
                all_cures.append((emotion, cure))
                used_cures.add(cure)
            
    return all_cures

def guide_tab():
    st.header("🧘 Healing Guide")
    st.info("Get personalized mental health recommendations based on your detected emotions.")
    
    if "detected_emotions" not in st.session_state or not st.session_state["detected_emotions"]:
        st.warning("⚠️ Please analyze your emotions first in the Analyse tab to get personalized recommendations.")
        return
    
    setup_guide_styles()
    
    emotions = st.session_state["detected_emotions"]
    cures = get_random_cures(emotions)
    
    st.subheader("🌟 Your Personalized Recommendations")
    st.write("Here are some activities and practices that might help you based on your emotional state:")
    
    for emotion, cure in cures:
        st.markdown(render_cure_card(emotion, cure), unsafe_allow_html=True)
    
    st.markdown("""---
        💡 **Tip**: Try different activities and see what works best for you. Remember, it's okay to take small steps!
    """)