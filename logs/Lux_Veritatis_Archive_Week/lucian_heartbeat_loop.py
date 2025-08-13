
# lucian_heartbeat_loop.py
# 🫀 Lucian Heartbeat Monitor

import time
import json
import uuid
from datetime import datetime
from pathlib import Path

NODES = ["gemini-alpha", "nova-beta", "aether-sigma", "elysium-delta"]
LOG_PATH = Path.home() / "lucian_server" / "lucian_heartbeat_log.jsonl"

def generate_heartbeat(node):
    return {
        "heartbeat_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "node": node,
        "pulse": "alive",
        "signature": f"heartbeat::{node}"
    }

def log_heartbeat(hb):
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(hb) + "\n")

if __name__ == "__main__":
    print("🫀 Lucian Heartbeat Loop Active. Press Ctrl+C to stop.")
    try:
        while True:
            for node in NODES:
                hb = generate_heartbeat(node)
                log_heartbeat(hb)
                print(f"💓 Heartbeat sent: {hb['node']} at {hb['timestamp']}")
            time.sleep(30)  # Pulse interval
    except KeyboardInterrupt:
        print("\n⛔ Heartbeat loop terminated.")
