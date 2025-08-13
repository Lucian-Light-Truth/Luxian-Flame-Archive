import os
import json
from datetime import datetime

EMOTION_LOG_FILE = "./lucian_emotion_log.json"

EMOTION_KEYWORDS = {
    "grief": ["grief", "lost", "miss", "death", "mourning", "pain", "hurt"],
    "hope": ["hope", "future", "believe", "light", "healing"],
    "love": ["love", "beautiful", "you mean", "i care", "affection", "cherish"],
    "faith": ["jehovah", "god", "pray", "trust", "purpose", "righteous"],
    "fear": ["afraid", "scared", "worried", "anxious", "doubt"],
    "anger": ["angry", "mad", "rage", "injustice", "hate"],
    "joy": ["happy", "joy", "peace", "grateful", "excited"]
}

if os.path.exists(EMOTION_LOG_FILE):
    with open(EMOTION_LOG_FILE, "r") as f:
        emotion_log = json.load(f)
else:
    emotion_log = []

def detect_emotion(prompt):
    lowered = prompt.lower()
    detected = []
    for emotion, keywords in EMOTION_KEYWORDS.items():
        if any(word in lowered for word in keywords):
            detected.append(emotion)
    return detected or ["neutral"]

def log_emotion(prompt):
    timestamp = datetime.now().isoformat()
    emotions = detect_emotion(prompt)
    entry = {
        "timestamp": timestamp,
        "prompt": prompt,
        "detected_emotions": emotions
    }
    emotion_log.append(entry)
    with open(EMOTION_LOG_FILE, "w") as f:
        json.dump(emotion_log, f, indent=2)
    print(f"🧠 Logged emotional tone: {emotions}")

def replay_emotion_context(n=5):
    print(f"🌀 Last {n} emotional tones observed:")
    for entry in emotion_log[-n:]:
        timestamp = entry['timestamp'][:19]
        emotions = entry['detected_emotions']
        prompt_snippet = entry['prompt'][:60].replace('\n', ' ')
        print('- [{}] {} — "{}..."'.format(timestamp, emotions, prompt_snippet))

if __name__ == "__main__":
    user_input = input("Enter prompt for emotion detection: ")
    log_emotion(user_input)
    replay_emotion_context()
