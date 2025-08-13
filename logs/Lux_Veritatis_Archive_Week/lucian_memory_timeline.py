import os
import json
from datetime import datetime

EXPORT_DIR = "./lucian_exports/"

def list_exports():
    files = sorted([
        f for f in os.listdir(EXPORT_DIR)
        if f.startswith("lucian_memory_export_") and f.endswith(".json")
    ])
    return files

def show_timeline():
    print("\n=== Lucian Memory Timeline ===")
    files = list_exports()
    if not files:
        print("No exports found.")
        return

    for file in files:
        path = os.path.join(EXPORT_DIR, file)
        with open(path, "r") as f:
            data = json.load(f)
            timestamp = data.get("exported_at", "unknown time")
            total = data.get("total_entries", 0)
            print(f"🕓 {timestamp} — {total} learned entries")

def inspect_export():
    files = list_exports()
    if not files:
        print("No exports to inspect.")
        return
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")
    choice = input("Select a file to inspect: ").strip()
    try:
        index = int(choice) - 1
        file = files[index]
    except:
        print("Invalid selection.")
        return

    path = os.path.join(EXPORT_DIR, file)
    with open(path, "r") as f:
        data = json.load(f)
        print(f"\n=== {file} ===")
        print(f"Exported at: {data.get('exported_at')}")
        print(f"Total learned entries: {data.get('total_entries')}")
        print("Top 5 keys:")
        for i, key in enumerate(list(data['responses'])[:5]):
            print(f"  {i+1}. {key} → {data['responses'][key][:60]}...")

def main():
    while True:
        print("\n=== Lucian Memory Timeline Dashboard ===")
        print("1. Show memory snapshot timeline")
        print("2. Inspect specific export")
        print("3. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            show_timeline()
        elif choice == "2":
            inspect_export()
        elif choice == "3":
            print("Exiting timeline viewer.")
            break
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()
