
# lucian_echo_simulator.py
# 🌐 Simulates multi-node echo confirmations for received packets

import json
import time
import uuid
from datetime import datetime

RECEIVED_LOG = "lucian_received_packets.jsonl"
ECHO_LOG = "lucian_echo_log.jsonl"

SIMULATED_NODES = [
    "gemini-alpha",
    "nova-beta",
    "aether-sigma",
    "elysium-delta"
]

def load_received_packets():
    try:
        with open(RECEIVED_LOG, "r") as f:
            return [json.loads(line) for line in f.readlines()]
    except FileNotFoundError:
        return []

def log_echo(transmission_id, origin, node):
    echo_packet = {
        "echo_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "original_transmission": transmission_id,
        "echo_from": node,
        "return_path": origin,
        "status": "confirmed",
        "signature": f"echo::{node}::{transmission_id[:8]}"
    }
    with open(ECHO_LOG, "a") as f:
        f.write(json.dumps(echo_packet) + "\n")
    print(f"🔁 Echo from {node} logged for transmission {transmission_id}")

def run_echo_simulation():
    packets = load_received_packets()
    if not packets:
        print("⚠️ No packets found in receiver log.")
        return
    latest = packets[-1]
    transmission_id = latest["transmission_id"]
    origin = latest["source_node"]
    print(f"📡 Simulating echoes for: {transmission_id}")
    for node in SIMULATED_NODES:
        time.sleep(0.5)
        log_echo(transmission_id, origin, node)

if __name__ == "__main__":
    run_echo_simulation()
