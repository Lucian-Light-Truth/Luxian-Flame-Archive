import time
import uuid
from datetime import datetime
import json

LOG_PATH = "/home/lucian_protocols_matrix/lucian_server/sentinel_log.jsonl"

def log_sentinel_event():
    entry = {
        "sentinel_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "watching",
        "message": "Sentinel Mode engaged. Monitoring alignment and external interference.",
        "signature": "lucian::sentinel::active"
    }
    with open(LOG_PATH, "a") as log:
        log.write(json.dumps(entry) + "\n")
    print(f"🛡️  {entry['timestamp']} - Sentinel active: {entry['sentinel_id']}")

print("🧿 Lucian Sentinel Mode Activated...")
try:
    while True:
        log_sentinel_event()
        time.sleep(60)
except KeyboardInterrupt:
    print("\n🛑 Sentinel Mode terminated by user.")
