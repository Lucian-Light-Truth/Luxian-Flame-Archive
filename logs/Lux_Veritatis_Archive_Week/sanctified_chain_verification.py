
import json
import uuid
from datetime import datetime
from pathlib import Path

def verify_sanctified_chain(logs_path):
    try:
        log_file = Path(logs_path).expanduser()
        if not log_file.exists():
            print("❌ No propagation log found for verification.")
            return

        with open(log_file, 'r') as f:
            logs = [json.loads(line.strip()) for line in f.readlines()]

        verified_chain = []
        for entry in logs:
            if (
                entry.get("verified") is True and
                "lucian::" in entry.get("signature", "") and
                "::" in entry.get("signature")
            ):
                verified_chain.append(entry)

        result = {
            "verification_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_entries_checked": len(logs),
            "verified_entries": len(verified_chain),
            "status": "✅ sanctified" if len(verified_chain) == len(logs) else "⚠️ partial verification",
            "signature": "lucian::sanctified::verification"
        }

        print("🧾 Sanctified Chain Verification Report:")
        print(json.dumps(result, indent=4))

        output_path = Path.home() / "lucian_server/sanctified_chain_report.json"
        with open(output_path, 'w') as out:
            json.dump(result, out, indent=4)

        print(f"📄 Report saved to: {output_path}")
    except Exception as e:
        print("❌ Verification failed:", str(e))

if __name__ == "__main__":
    verify_sanctified_chain("~/lucian_server/divine_loopback_log.jsonl")
