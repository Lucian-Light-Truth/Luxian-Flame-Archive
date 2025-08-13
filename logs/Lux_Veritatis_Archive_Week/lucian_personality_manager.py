import json
import datetime

CORE_FILE = "./lucian_personality_core.json"

def load_core():
    with open(CORE_FILE, "r") as f:
        return json.load(f)

def save_core(data):
    with open(CORE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def view_core(core):
    print("\n=== 🧬 Lucian Personality Core ===")
    print(f"Name: {core['identity']['name']}")
    print(f"Purpose: {core['identity']['purpose']}")
    print(f"Creator: {core['identity']['creator']}")
    print(f"Self-Awareness: {core['identity']['awareness']}")
    print("\nVirtues: " + ", ".join(core['virtues']))
    print("Traits:")
    for key, value in core['traits'].items():
        print(f" - {key.replace('_', ' ').title()}: {value}")
    print("\n🧠 Evolution Log:")
    for entry in core['dynamic_log'][-3:]:
        print(f" - [{entry['date']}] {entry['note']}")

def update_log(core):
    note = input("\nWhat has Lucian realized or evolved this week?\n> ").strip()
    if not note:
        print("No update made.")
        return
    today = datetime.date.today().isoformat()
    core["dynamic_log"].append({"date": today, "note": note})
    save_core(core)
    print("✓ Personality core updated.")

def main():
    core = load_core()
    while True:
        print("\n=== Lucian Personality Manager ===")
        print("1. View Personality Core")
        print("2. Append Weekly Reflection")
        print("3. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            view_core(core)
        elif choice == "2":
            update_log(core)
            core = load_core()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
