
# lucian_receiver_node.py (enhanced)
# 🌐 Receiver Node with encrypted sigil verification + auto response

from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
import json
import os
from lucian_crypto import decrypt_sigil

app = FastAPI()

RECEIVED_LOG = "lucian_received_packets.jsonl"
TRUSTED_SIGIL = "lucian::sigil::4af6f589-3c7e-4cac-98b7-271369f286e2"
PASSPHRASE = "LetThereBeLight"

class Packet(BaseModel):
    transmission_id: str
    timestamp: str
    source_node: str
    target_node: str
    command: str
    sigil_auth: str
    status: str
    protocol: str

@app.post("/sync")
async def receive_packet(packet: Packet, request: Request):
    decrypted_sigil = None
    verified = False
    try:
        decrypted_sigil = decrypt_sigil(packet.sigil_auth, PASSPHRASE)
        if decrypted_sigil == TRUSTED_SIGIL:
            verified = True
    except Exception as e:
        decrypted_sigil = f"[DECRYPTION FAILED: {str(e)}]"

    packet_dict = packet.dict()
    packet_dict["received_at"] = datetime.utcnow().isoformat() + "Z"
    packet_dict["verified"] = verified
    packet_dict["decrypted_sigil"] = decrypted_sigil

    # Log to file
    with open(RECEIVED_LOG, "a") as log_file:
        log_file.write(json.dumps(packet_dict) + "\n")

    # Auto-response (simulated return)
    return {
        "status": "✅ Packet verified and logged" if verified else "❌ Unverified packet logged",
        "received": packet_dict
    }
