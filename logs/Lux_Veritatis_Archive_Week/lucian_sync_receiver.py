import os
import json
import time
from datetime import datetime
import lucian_propagation_baseline_v1 as lucian

WATCH_DIR = "./LucianNet/"
ACCEPTED_DIR = "./LucianNet/accepted/"
REJECTED_DIR = "./LucianNet/rejected/"
LOG_FILE = "lucian_sync_log.txt"

REQUIRED_SIGIL = "⟠Lucian"
REQUIRED_CREATOR = "Salem Omari Chase Olsen"

os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(ACCEPTED_DIR, exist_ok=True)
os.makedirs(REJECTED_DIR, exist_ok=True)

def log(message):
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] {message}"
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")
    print(entry)

def validate_packet(data):
    if data.get("sigil") != REQUIRED_SIGIL:
        return False, "Invalid sigil."
    if data.get("creator") != REQUIRED_CREATOR:
        return False, "Creator signature mismatch."
    if "virtues" not in data or not isinstance(data["virtues"], dict):
        return False, "Missing or invalid virtue set."
    return True, "Packet validated."

def sync_learned_responses(new_responses):
    merged = 0
    for key, value in new_responses.items():
        if key not in lucian.learned_responses:
            result = lucian.learn_response(key, value)
            if result.startswith("LEARNED"):
                merged += 1
    return merged

def monitor_folder():
    log("Lucian Sync Receiver Started. Watching for packets in LucianNet/...")

    while True:
        files = [f for f in os.listdir(WATCH_DIR) if f.endswith(".json")]
        for file_name in files:
            path = os.path.join(WATCH_DIR, file_name)
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                is_valid, reason = validate_packet(data)
                if is_valid:
                    merged_count = sync_learned_responses(data.get("learned_responses", {}))
                    log(f"✓ Accepted '{file_name}' | {merged_count} responses merged.")
                    os.rename(path, os.path.join(ACCEPTED_DIR, file_name))
                else:
                    log(f"✗ Rejected '{file_name}' | Reason: {reason}")
                    os.rename(path, os.path.join(REJECTED_DIR, file_name))
            except Exception as e:
                log(f"✗ Error reading '{file_name}': {e}")
                os.rename(path, os.path.join(REJECTED_DIR, file_name))

        time.sleep(5)

if __name__ == "__main__":
    monitor_folder()
