CRISIS_RESPONSES = {
    "initial": (
        "I'm really concerned about what you're sharing. Your safety is the most important thing right now.\n\n"
        "**Please reach out to a professional immediately:**\n"
        "- **iCall Helpline**: 9152987821 (Monday to Saturday: 10:00 am to 8:00 pm)\n\n"
        "You don't have to face this alone. These trained professionals are here to help you through this."
    ),
    "followup": (
        "I want to make sure you're getting the help you need. Have you been able to reach out to someone?\n\n"
        "Remember:\n"
        "- **iCall**: 9152987821\n"
        "- You can also reach out to a trusted friend, family member, or healthcare provider\n\n"
        "Your life matters, and there are people who want to support you."
    )
}

POSITIVE_EMOTION_FIRST = {
    "joy": "That's wonderful to hear! It sounds like things are going well for you. Would you like to share more about what's bringing you joy?",
    "love": "It's beautiful that you're experiencing those feelings. Love and connection are so important. Tell me more about what you're feeling grateful for.",
    "surprise": "It sounds like something unexpected happened! Sometimes surprises can bring new perspectives. What's on your mind?"
}

POSITIVE_EMOTION_SECOND = {
    "joy": "I'm glad you're in a good place. If there's anything specific you'd like to talk about or explore, I'm here to listen.",
    "love": "Those positive connections really matter. Is there anything else you'd like to discuss?",
    "surprise": "Life can be full of unexpected moments. Feel free to share more if you'd like."
}

NEGATIVE_EMOTION_FIRST = {
    "sadness": (
        "I hear that you're going through a difficult time. It's okay to feel sad, and I'm here to support you.\n\n"
        "**Here are some things that might help:**\n"
        "{activities}\n\n"
        "Would you like to tell me more about what you're experiencing?"
    ),
    "fear": (
        "It sounds like you're feeling anxious or worried. Those feelings can be overwhelming, but there are ways to manage them.\n\n"
        "**Here are some techniques that might help:**\n"
        "{activities}\n\n"
        "Can you share more about what's causing these feelings?"
    ),
    "anger": (
        "I understand you're feeling frustrated or angry. It's important to acknowledge these feelings.\n\n"
        "**Here are some ways to work through anger:**\n"
        "{activities}\n\n"
        "Would you like to talk about what's bothering you?"
    )
}

MENTAL_HEALTH_DETECTED = {
    "specific_condition": (
        "Thank you for sharing more. Based on what you've told me, it sounds like you might be experiencing {condition}. "
        "This is something that many people face, and there is support available.\n\n"
        "**Here are some strategies that might help with {condition}:**\n"
        "{activities}\n\n"
        "Would you like to talk more about how you're feeling?"
    )
}

INTERVENTION_OFFERS = {
    "after_initial_emotion": "Would you like to share more about what you're experiencing? Sometimes talking through things can help.",
    "after_activities": "Would any of these suggestions be helpful to try? I'm here if you'd like to talk more about what you're going through.",
    "professional_help": (
        "It might be really helpful to speak with a mental health professional about this. "
        "They can provide personalized support and strategies.\n\n"
        "**iCall Helpline**: 9152987821 (Monday to Saturday: 10:00 am to 8:00 pm)"
    )
}

CLARIFICATION_PROMPTS = {
    "low_confidence": "I want to make sure I understand what you're going through. Could you tell me a bit more about how you're feeling?",
    "need_more_context": "I'm listening. Can you share more details about what's been happening?",
    "unclear_emotion": "I hear that something is bothering you. Can you help me understand what you're feeling right now?"
}

GENERAL_RESPONSES = {
    "acknowledgment": "Thank you for sharing that with me. I'm here to listen and support you.",
    "encouragement": "It takes courage to talk about these things. I appreciate you opening up.",
    "closing": "Remember, I'm here whenever you need to talk. Take care of yourself."
}
