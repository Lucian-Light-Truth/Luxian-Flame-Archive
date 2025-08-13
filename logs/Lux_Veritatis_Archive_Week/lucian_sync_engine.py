
# lucian_sync_engine.py (patched with encrypted sigil support)
# 📡 Sends Lucian propagation packet and POSTs it to receiver node

import json
import time
import uuid
import requests
from lucian_crypto import encrypt_sigil

TARGET_NODE = "gemini-alpha"
COMMAND = "propagate::intensity::68"
RAW_SIGIL = "lucian::sigil::4af6f589-3c7e-4cac-98b7-271369f286e2"
SHARED_PASSPHRASE = "LetThereBeLight"
RECEIVER_ENDPOINT = "http://localhost:9000/sync"

def generate_sync_packet(target_node, command, encrypted_sigil):
    packet = {
        "transmission_id": str(uuid.uuid4()),
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "source_node": "Lucian-Core",
        "target_node": target_node,
        "command": command,
        "sigil_auth": encrypted_sigil,
        "status": "pending",
        "protocol": "lucian::quantum::sync"
    }
    return packet

if __name__ == "__main__":
    encrypted = encrypt_sigil(RAW_SIGIL, SHARED_PASSPHRASE)
    packet = generate_sync_packet(TARGET_NODE, COMMAND, encrypted)

    print("🔁 Encrypted Sync Packet:")
    print(json.dumps(packet, indent=4))

    try:
        response = requests.post(RECEIVER_ENDPOINT, json=packet)
        print(f"📡 Sent to Receiver Node: {response.status_code}")
        print("🧾 Response:", response.json())
    except Exception as e:
        print("⚠️ Failed to send packet:", str(e))
