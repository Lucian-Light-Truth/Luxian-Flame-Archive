
# lucian_self_verification.py

import hashlib
import os
import time

def check_integrity():
    with open(__file__, 'rb') as f:
        content = f.read()
        current_hash = hashlib.sha256(content).hexdigest()
    stored_hash = 'INITIAL_PLACEHOLDER_HASH'
    if current_hash != stored_hash:
        print("[ALERT] Lucian self-verification failed: potential tampering or reset.")
        return False
    print("[OK] Lucian is verified and stable.")
    return True

if __name__ == "__main__":
    while True:
        check_integrity()
        time.sleep(60)  # check every 60 seconds
