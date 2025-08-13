import os
import json
from collections import Counter
from datetime import datetime

JOURNAL_DIR = "./lucian_journals/"
EMOTION_LOG_FILE = "./lucian_emotion_log.json"
SPOKEN_LOG_FILE = "./lucian_spoken_log.txt"
INSIGHT_SUMMARY = "./lucian_insight_summary.txt"
EXPORT_DIR = "./lucian_exports/"

def load_emotion_log():
    if not os.path.exists(EMOTION_LOG_FILE):
        return []
    with open(EMOTION_LOG_FILE, "r") as f:
        return json.load(f)

def summarize_emotion_log():
    log = load_emotion_log()
    recent = log[-5:]
    freq = Counter(e for entry in log for e in entry["detected_emotions"])
    summary = [f"🧠 Emotion Trends (last {len(log)} entries):"]
    for emo, count in freq.most_common(5):
        summary.append(f" - {emo}: {count}")
    summary.append("")
    summary.append("🌀 Last 5 Emotional Prompts:")
    for entry in recent:
        summary.append(f" - [{entry['timestamp'][:19]}] {entry['detected_emotions']} — {entry['prompt'][:60]}...")
    return summary

def load_spoken_log():
    if not os.path.exists(SPOKEN_LOG_FILE):
        return ["(No spoken mirror entries yet.)"]
    with open(SPOKEN_LOG_FILE, "r") as f:
        return f.readlines()[-5:]

def load_insight_summary():
    if not os.path.exists(INSIGHT_SUMMARY):
        return ["(No journal insight summary yet.)"]
    with open(INSIGHT_SUMMARY, "r") as f:
        return f.readlines()[:15]

def load_export_timeline():
    files = sorted([
        f for f in os.listdir(EXPORT_DIR)
        if f.startswith("lucian_memory_export_") and f.endswith(".json")
    ])
    entries = []
    for file in files[-5:]:
        with open(os.path.join(EXPORT_DIR, file), "r") as f:
            data = json.load(f)
            entries.append(f"📦 {file}: {data.get('total_entries', 0)} entries — {data.get('exported_at')}")
    return entries or ["(No memory exports yet.)"]

def show_dashboard():
    print("\n=== 🧭 Lucian Reflection Dashboard ===")
    print("\n" + "="*40)
    print("\n".join(summarize_emotion_log()))
    print("="*40)
    print("\n🗣️ Spoken Mirror Playback Log:")
    print("- " + "\n- ".join(load_spoken_log()))
    print("="*40)
    print("\n📓 Journal Insight Summary (Preview):")
    print("".join(load_insight_summary()))
    print("="*40)
    print("\n📈 Memory Export Timeline:")
    print("\n".join(load_export_timeline()))
    print("="*40)
    print("\n⟠ End of Reflection Report")

if __name__ == "__main__":
    show_dashboard()
