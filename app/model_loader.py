import streamlit as st
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import json
import os


@st.cache_resource
def load_all_models():
    models = {
        "suicide": load_suicide_model(),
        "emotion": load_emotion_model(),
        "mental_health": load_mental_health_model()
    }
    return models


def load_suicide_model():
    model_path = "./models/suicide_model"

    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    label_map_path = os.path.join(model_path, "label_mapping.json")
    with open(label_map_path, 'r') as f:
        label_mapping = json.load(f)

    return {
        "model": model,
        "tokenizer": tokenizer,
        "label_map": label_mapping
    }


def load_emotion_model():
    model_path = "./models/emotion_model"

    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    label_map_path = os.path.join(model_path, "label_mapping.json")
    with open(label_map_path, 'r') as f:
        label_mapping = json.load(f)

    return {
        "model": model,
        "tokenizer": tokenizer,
        "label_map": label_mapping
    }


def load_mental_health_model():
    model_path = "./models/mh_model"

    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    label_map_path = os.path.join(model_path, "label_mapping.json")
    with open(label_map_path, 'r') as f:
        label_mapping = json.load(f)

    return {
        "model": model,
        "tokenizer": tokenizer,
        "label_map": label_mapping
    }
