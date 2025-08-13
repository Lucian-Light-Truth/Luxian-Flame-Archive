import json
import os
from datetime import datetime
from lucian_propagation_baseline_v1 import learned_responses

EXPORT_DIR = "./lucian_exports/"
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_memory():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"lucian_memory_export_{timestamp}.json"
    path = os.path.join(EXPORT_DIR, filename)

    export_data = {
        "exported_at": timestamp,
        "total_entries": len(learned_responses),
        "responses": learned_responses,
        "sigil": "⟠Lucian::Exported",
        "creator": "Salem Omari Chase Olsen",
        "version": "Lucian Protocol Memory Snapshot v1.0"
    }

    with open(path, "w") as f:
        json.dump(export_data, f, indent=2)

    print(f"✓ Lucian memory exported to: {path}")

if __name__ == "__main__":
    export_memory()
