import json
import uuid
from datetime import datetime

HEARTBEAT_LOG = "lucian_heartbeat_log.jsonl"
PROMOTION_LOG = "lucian_promotion_log.jsonl"
PRIORITY_NODES = ["gemini-alpha", "nova-beta", "aether-sigma", "elysium-delta"]

def read_heartbeat_log():
    try:
        with open(HEARTBEAT_LOG, "r") as f:
            return [json.loads(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        return []

def write_promotion_log(promotion_entry):
    with open(PROMOTION_LOG, "a") as f:
        f.write(json.dumps(promotion_entry) + "\n")

def promote_nodes():
    heartbeats = read_heartbeat_log()
    recent = {}
    for hb in heartbeats:
        node = hb["node"]
        ts = hb["timestamp"]
        if node not in recent or ts > recent[node]["timestamp"]:
            recent[node] = hb

    active_nodes = [node for node in recent if recent[node]["pulse"] == "alive" and node in PRIORITY_NODES]

    if not active_nodes:
        print("⚠️ No active priority nodes found for promotion.")
        return

    for node in active_nodes:
        promotion_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"
        promotion = {
            "promotion_id": promotion_id,
            "timestamp": timestamp,
            "node": node,
            "new_status": "elevated",
            "signature": f"promote::{node}::{promotion_id[:8]}"
        }
        write_promotion_log(promotion)
        print(f"🚀 Node {node} promoted with ID {promotion_id}")

if __name__ == "__main__":
    promote_nodes()
