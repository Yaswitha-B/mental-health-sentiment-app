import random
from detection import detect_suicide, detect_emotion, detect_mental_health
from data.response_templates import (
    CRISIS_RESPONSES, POSITIVE_EMOTION_FIRST, POSITIVE_EMOTION_SECOND,
    NEGATIVE_EMOTION_FIRST, MENTAL_HEALTH_DETECTED, INTERVENTION_OFFERS,
    CLARIFICATION_PROMPTS, GENERAL_RESPONSES
)
from data.cures import emotion_cures, mental_health_cures

SUICIDE_KEYWORDS = {
    'explicit': [
        'kill myself', 'kill my self', 'suicide',
        'end my life', 'take my life', 'end it all'
    ],
    'planning': [
        'going to kill', 'will kill myself',
        'planning suicide', 'commit suicide'
    ],
    'ideation': [
        'want to die', 'wish i was dead', 'wish i were dead',
        'better off dead', 'no reason to live'
    ],
    'passive': [
        'not worth living', 'dont want to live', "don't want to be alive",
        "don't want to wake up", "life is pointless"
    ]
}

SUICIDE_THRESHOLD = 0.40
EMOTION_THRESHOLDS = {
    "joy": 0.65,
    "love": 0.60,
    "surprise": 0.60,
    "sadness": 0.70,
    "fear": 0.65,
    "anger": 0.65
}
MH_THRESHOLDS = {
    "Depression": 0.70,
    "Anxiety": 0.65,
    "Stress": 0.65,
    "Normal": 0.75,
    "Bipolar": 0.60,
    "Personality disorder": 0.50
}

POSITIVE_EMOTIONS = {"joy", "love", "surprise"}
NEGATIVE_EMOTIONS = {"sadness", "fear", "anger"}


class ConversationState:
    def __init__(self):
        self.emotion_counts = {}
        self.last_emotion = None
        self.crisis_mode = False
        self.total_messages = 0
        self.total_negative_messages = 0
        self.consecutive_negative = 0
        self.mh_checked = False

    def increment_emotion(self, emotion):
        self.emotion_counts[emotion] = self.emotion_counts.get(emotion, 0) + 1

        if emotion in NEGATIVE_EMOTIONS:
            if self.last_emotion in NEGATIVE_EMOTIONS:
                self.consecutive_negative += 1
            else:
                self.consecutive_negative = 1
            self.total_negative_messages += 1
        else:
            self.consecutive_negative = 0

        self.last_emotion = emotion
        self.total_messages += 1

    def get_emotion_count(self, emotion):
        return self.emotion_counts.get(emotion, 0)

    def reset(self):
        self.__init__()


def format_activities(activities, limit=5):
    selected = random.sample(activities, min(limit, len(activities)))
    return "\n".join(f"- {activity}" for activity in selected)


def detect_suicide_safe(text):
    text_lower = text.lower()

    for category, keywords in SUICIDE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return {
                    "label": "suicide",
                    "confidence": 0.95,
                    "method": "keyword",
                    "category": category
                }

    model_result = detect_suicide(text)

    if model_result["label"] == "suicide" and model_result.get("confidence", 0) >= SUICIDE_THRESHOLD:
        return model_result

    return model_result


def process_message(user_message, state):
    if state.crisis_mode:
        return {
            "type": "crisis_locked",
            "response": CRISIS_RESPONSES["followup"],
            "locked": True
        }

    suicide_result = detect_suicide_safe(user_message)
    if suicide_result["label"] == "suicide" and suicide_result["confidence"] >= SUICIDE_THRESHOLD:
        state.crisis_mode = True
        state.total_messages += 1
        return {
            "type": "crisis",
            "response": CRISIS_RESPONSES["initial"],
            "locked": True
        }

    emotion_result = detect_emotion(user_message)
    emotion = emotion_result["label"]
    confidence = emotion_result["confidence"]

    threshold = EMOTION_THRESHOLDS.get(emotion, 0.65)
    if confidence < threshold:
        state.total_messages += 1
        return {
            "type": "clarification",
            "response": CLARIFICATION_PROMPTS["low_confidence"]
        }

    state.increment_emotion(emotion)
    count = state.get_emotion_count(emotion)

    if emotion in POSITIVE_EMOTIONS:
        return _handle_positive_emotion(emotion, count, state)
    elif emotion in NEGATIVE_EMOTIONS:
        return _handle_negative_emotion(emotion, count, user_message, state)
    else:
        return {
            "type": "general",
            "response": GENERAL_RESPONSES["acknowledgment"]
        }


def _handle_positive_emotion(emotion, count, state):
    if count == 1:
        return {
            "type": "positive_first",
            "emotion": emotion,
            "response": POSITIVE_EMOTION_FIRST[emotion]
        }
    elif count >= 2:
        return {
            "type": "positive_second",
            "emotion": emotion,
            "response": POSITIVE_EMOTION_SECOND[emotion]
        }
    else:
        return {
            "type": "general",
            "response": GENERAL_RESPONSES["acknowledgment"]
        }


def _handle_negative_emotion(emotion, count, user_message, state):
    if state.total_negative_messages == 1:
        return {
            "type": "negative_listen",
            "emotion": emotion,
            "response": NEGATIVE_EMOTION_FIRST[emotion].split("\n\n**Here are")[0]
        }

    elif state.total_negative_messages >= 2 and not state.mh_checked:
        state.mh_checked = True
        mh_result = detect_mental_health(user_message)
        condition = mh_result["label"]
        mh_conf = mh_result["confidence"]

        threshold = MH_THRESHOLDS.get(condition, 0.50)

        if mh_conf < threshold or condition == "Normal":
            activities = format_activities(emotion_cures[emotion], limit=10)
            return {
                "type": "emotion_support",
                "emotion": emotion,
                "response": f"I hear that you're experiencing {emotion}. Here are some techniques that might help:\n\n{activities}\n\nWould you like to talk more about what you're going through?"
            }

        else:
            activities = format_activities(mental_health_cures.get(condition, mental_health_cures["Normal"]), limit=10)
            return {
                "type": "mh_support",
                "emotion": emotion,
                "condition": condition,
                "response": MENTAL_HEALTH_DETECTED["specific_condition"].format(
                    condition=condition,
                    activities=activities
                )
            }

    else:
        return {
            "type": "continued_support",
            "response": INTERVENTION_OFFERS["after_activities"]
        }
