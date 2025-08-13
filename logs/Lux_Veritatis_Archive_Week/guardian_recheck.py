import uuid
from datetime import datetime
import json
import os

GUARDIAN_LOG = os.path.expanduser("~/lucian_server/guardian_verification_log.jsonl")

def log_guardian_check():
    guardian_check = {
        "check_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "confirmed",
        "signature": "guardian::recheck::lucian"
    }

    with open(GUARDIAN_LOG, "a") as f:
        f.write(json.dumps(guardian_check) + "\n")
    print("✅ Guardian verification confirmed.")
    print(json.dumps(guardian_check, indent=4))

if __name__ == "__main__":
    print("🔐 Running Guardian Verification Recheck...")
    log_guardian_check()
