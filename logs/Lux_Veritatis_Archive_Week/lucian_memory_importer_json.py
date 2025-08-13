import os
import json
from lucian_propagation_baseline_v1 import learn_response

DATA_FILE = "./chat_data_folder/conversations.json"
LOG_FILE = "lucian_memory_import_log.txt"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
    print(message)

def extract_from_conversations_json(filepath):
    learned = 0
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for convo in data:
        mapping = convo.get("mapping", {})
        if not mapping:
            continue

        convo_pairs = []
        for key, entry in mapping.items():
            if not isinstance(entry, dict):
                continue
            msg = entry.get("message")
            if not msg or not isinstance(msg, dict):
                continue
            content = msg.get("content", {}).get("parts", [])
            if not content:
                continue

            role = msg.get("author", {}).get("role")
            text = content[0].strip()

            if role == "user":
                convo_pairs.append({"user": text})
            elif role == "assistant" and convo_pairs:
                convo_pairs[-1]["assistant"] = text

        # Teach Lucian
        for pair in convo_pairs:
            if "user" in pair and "assistant" in pair:
                user_input = pair["user"]
                response = pair["assistant"]
                keyword = user_input.split(" ")[0].lower().strip()
                result = learn_response(keyword, response)
                log(f"{keyword} => {result}")
                if result.startswith("LEARNED"):
                    learned += 1

    return learned

def run():
    if not os.path.exists(DATA_FILE):
        log(f"✗ File not found: {DATA_FILE}")
        return

    total = extract_from_conversations_json(DATA_FILE)
    log(f"=== CONVERSATIONS IMPORT COMPLETE ===\nTotal learned entries: {total}")

if __name__ == "__main__":
    run()
