import torch
from torch.nn.functional import softmax

_models = None

def initialize_models(models):
    global _models
    _models = models

detect_suicide = lambda text: _predict(text, _models["suicide"])
detect_emotion = lambda text: _predict(text, _models["emotion"])
detect_mental_health = lambda text: _predict(text, _models["mental_health"])


def _predict(text, model_data):
    model = model_data["model"]
    tokenizer = model_data["tokenizer"]
    id2label = model_data["label_map"]["id2label"]

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    probs = softmax(logits, dim=1)
    predicted_idx = probs.argmax().item()
    confidence = probs[0][predicted_idx].item()
    label = id2label[str(predicted_idx)]

    return {"label": label, "confidence": confidence}
