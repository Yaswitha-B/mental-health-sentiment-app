import streamlit as st
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from data.emotion_labels import GOEMOTIONS_LABELS
from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if API_KEY is None:
    raise ValueError("OpenRouter API Key not found!")

EMOTION_THRESHOLD = 0.6
MAX_HISTORY_TOKENS = 512

model = AutoModelForSequenceClassification.from_pretrained(
    "bsingh/roberta_goEmotion",
    problem_type="multi_label_classification"
)
tokenizer = AutoTokenizer.from_pretrained("bsingh/roberta_goEmotion")

classifier = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    return_all_scores=True
)

def get_user_messages():
    if not st.session_state.get("chat_history"):
        return []
    return [msg["content"] for msg in st.session_state["chat_history"] if msg["role"] == "user"]

def analyze_emotions(text):
    if not text.strip():
        return []
    scores = classifier(text)[0]
    return [
        (GOEMOTIONS_LABELS.get(item["label"], item["label"]), item["score"])
        for item in scores if item["score"] >= EMOTION_THRESHOLD
    ]

def render_emotion_card(emotion, score):
    percentage = int(score * 100)
    return f"""
        <div class='emotion-card'>
            <div class='emotion-label'>{emotion}</div>
            <div class='emotion-score'>Confidence: {percentage}%</div>
            <div class='progress-bar-bg'>
                <div class='progress-bar' style='width: {percentage}%'></div>
            </div>
        </div>
    """

def setup_ui_styles():
    st.markdown("""
        <style>
        .emotion-card {
            padding: 1rem;
            border-radius: 10px;
            background: linear-gradient(145deg, #ffffff, #f0f0f0);
            box-shadow: 5px 5px 10px #d9d9d9, -5px -5px 10px #ffffff;
            margin: 10px 0;
            transition: transform 0.2s;
        }
        .emotion-card:hover { transform: translateY(-2px); }
        .emotion-label {
            font-size: 1.1em;
            color: #1f1f1f;
            text-transform: capitalize;
        }
        .emotion-score { font-size: 0.9em; color: #4a4a4a; }
        .progress-bar-bg {
            background: #f0f0f0;
            border-radius: 5px;
            margin-top: 5px;
        }
        .progress-bar {
            background: linear-gradient(90deg, #3498db, #2980b9);
            height: 10px;
            border-radius: 5px;
            transition: width 0.5s ease-in-out;
        }
        </style>
    """, unsafe_allow_html=True)

def display_emotions(emotions):
    if not emotions:
        st.info("No significant emotions detected in the conversation.")
        return

    setup_ui_styles()
    for emotion, score in emotions:
        st.markdown(render_emotion_card(emotion, score), unsafe_allow_html=True)

def summerize_user_messages(messages):
    try:
        context = "You are an expert summarizer and psychologist. Analyze the following user messages, focusing on emotional patterns and key concerns. Do not guess any emotions and convey what user says. Provide a concise summary (max 512 tokens) that captures the emotional journey."

        messages_text = "\n".join(messages)

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": context},
                    {"role": "user", "content": messages_text}
                ],
                "temperature": 0.7,
                "max_tokens": MAX_HISTORY_TOKENS
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        return f"Error generating summary: {str(e)}"

def analyse_tab():
    st.header("🔎 Emotion Analysis")
    st.info("Analyze emotions expressed in your chat messages.")

    user_messages = get_user_messages()
    if not user_messages:
        st.warning("Start a conversation in the chat tab to analyze emotions.")
        return

    if st.button("Analyze Messages", key="analyse_btn"):
        with st.spinner("Analyzing emotions..."):
            summary = summerize_user_messages(user_messages)
            emotions = analyze_emotions(summary)
            st.subheader("📊 Detected Emotions")
            display_emotions(emotions)
