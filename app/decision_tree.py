import random
from detection import detect_suicide, detect_emotion, detect_mental_health
from data.response_templates import CRISIS_RESPONSES
from data.cures import emotion_cures, mental_health_cures


SUICIDE_THRESHOLD = 0.65
FORCE_PROPOSAL_TURNS = 3

SUICIDE_KEYWORDS = [
    "want to die",
    "want to end it all",
    "end it all",
    "kill myself",
    "suicide",
    "take my life",
    "don't want to live",
    "cant do this anymore"
]


class ConversationState:
    def __init__(self):
        self.crisis_mode = False

        self.emotion_scores = {}
        self.mh_scores = {}

        self.negated = set()

        self.turns = 0

        self.awaiting_confirmation = False
        self.proposed_type = None
        self.proposed_label = None

def normalize_mh_label(label):
    if not label:
        return None
    return label.strip().title()


def format_activities(activities, limit=8):
    if not activities:
        return ""
    chosen = random.sample(activities, min(limit, len(activities)))
    return "\n".join(f"- {a}" for a in chosen)


def reset_context(state):
    state.emotion_scores.clear()
    state.mh_scores.clear()
    state.negated.clear()
    state.turns = 0
    state.awaiting_confirmation = False
    state.proposed_type = None
    state.proposed_label = None


def choose_dominant(state):
    for label, _ in sorted(state.mh_scores.items(), key=lambda x: x[1], reverse=True):
        if ("mental_health", label) not in state.negated:
            return "mental_health", label

    for label, _ in sorted(state.emotion_scores.items(), key=lambda x: x[1], reverse=True):
        if ("emotion", label) not in state.negated:
            return "emotion", label

    return None, None


def process_message(user_message, state):

    if state.crisis_mode:
        return {
            "type": "crisis_locked",
            "response": CRISIS_RESPONSES["followup"],
            "locked": True
        }

    if not state.awaiting_confirmation:
        text = user_message.lower()

        if any(kw in text for kw in SUICIDE_KEYWORDS):
            state.crisis_mode = True
            return {
                "type": "crisis",
                "response": CRISIS_RESPONSES["initial"],
                "locked": True
            }

        suicide = detect_suicide(user_message)
        if suicide["label"] == "suicide" and suicide["confidence"] >= SUICIDE_THRESHOLD:
            state.crisis_mode = True
            return {
                "type": "crisis",
                "response": CRISIS_RESPONSES["initial"],
                "locked": True
            }

    if state.awaiting_confirmation:
        reply = user_message.strip().lower()

        if reply in {"yes", "y"} and state.proposed_label and state.proposed_type:
            label = state.proposed_label
            p_type = state.proposed_type

            if p_type == "mental_health":
                acts = format_activities(mental_health_cures.get(label, []))
            else:
                acts = format_activities(emotion_cures.get(label, []))

            reset_context(state)

            return {
                "type": f"{p_type}_support",
                "response": (
                    f"This appears to be {label.lower()}.\n\n"
                    f"{acts}\n\n"
                    "The analysis has been reset. You may continue."
                )
            }

        if reply in {"no", "n"} and state.proposed_label and state.proposed_type:
            state.negated.add((state.proposed_type, state.proposed_label))

            if state.proposed_type == "mental_health":
                state.mh_scores.pop(state.proposed_label, None)
            else:
                state.emotion_scores.pop(state.proposed_label, None)

            state.awaiting_confirmation = False
            state.proposed_label = None
            state.proposed_type = None

            return {
                "type": "analysis",
                "response": "Understood. More context is needed. Please continue."
            }

        state.awaiting_confirmation = False
        state.proposed_label = None
        state.proposed_type = None
        
    state.turns += 1

    emo = detect_emotion(user_message)
    state.emotion_scores[emo["label"]] = (
        state.emotion_scores.get(emo["label"], 0.0) + emo["confidence"]
    )

    mh = detect_mental_health(user_message)
    mh_label = normalize_mh_label(mh["label"])

    if mh_label and mh_label != "Normal" and mh["confidence"] >= 0.5:
        state.mh_scores[mh_label] = (
            state.mh_scores.get(mh_label, 0.0) + mh["confidence"]
        )

    p_type, p_label = choose_dominant(state)

    if p_label and state.turns >= FORCE_PROPOSAL_TURNS:
        state.awaiting_confirmation = True
        state.proposed_type = p_type
        state.proposed_label = p_label

        label_text = p_label.lower().replace("_", " ")

        return {
            "type": "confirm",
            "response": (
                f"Based on what you've shared, this may be {label_text}. "
                "Am I right? (Yes / No)"
            )
        }

    return {
        "type": "analysis",
        "response": "More context is needed to continue the analysis. Please continue."
    }
