import os
import json
from datetime import datetime
from lucian_propagation_baseline_v1 import learned_responses

JOURNAL_DIR = "./lucian_journals/"
LOG_FILE = "./lucian_memory_import_log.txt"
MIRROR_SCRIPT_PATH = "./lucian_mirror_mode.py"
SPOKEN_MIRROR_SCRIPT = "./lucian_spoken_mirror.py"
SPOKEN_LOG_FILE = "./lucian_spoken_log.txt"
REFLECTION_DASHBOARD_SCRIPT = "./lucian_reflection_dashboard.py"
PERSONALITY_MANAGER_SCRIPT = "./lucian_personality_manager.py"

def list_journals():
    files = sorted([
        f for f in os.listdir(JOURNAL_DIR)
        if f.startswith("lucian_journal_") and f.endswith(".txt")
    ])
    print("\n📜 Available Journals:")
    for f in files:
        print(" -", f)

def show_journal(filename):
    path = os.path.join(JOURNAL_DIR, filename)
    if not os.path.exists(path):
        print(f"✗ Not found: {filename}")
        return
    print(f"\n📝 {filename}\n" + "-"*40)
    with open(path, "r") as f:
        print(f.read())

def show_memory_stats():
    print("\n🧠 Memory Insight:")
    print(f"Total unique learned entries: {len(learned_responses)}")

    freq = {}
    for key in learned_responses:
        first = key.strip().lower().split(" ")[0]
        if len(first) > 1:
            freq[first] = freq.get(first, 0) + 1

    top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n🔑 Top 10 most common keywords:")
    for word, count in top:
        print(f"  {word}: {count}")

def read_log_summary():
    if not os.path.exists(LOG_FILE):
        print("\n(No import log found.)")
        return
    print("\n📂 Memory Import Log Summary:")
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    learned = [line for line in lines if "LEARNED:" in line]
    rejected = [line for line in lines if "REJECTED:" in line]
    print(f" - Learned entries: {len(learned)}")
    print(f" - Rejected entries: {len(rejected)}")

def trigger_mirror_mode():
    print("\n🪞 Triggering Lucian Mirror Mode...")
    result = os.system(f"python3 {MIRROR_SCRIPT_PATH}")
    if result == 0:
        print("✓ Mirror Mode journal created.")
    else:
        print("✗ Mirror Mode failed to execute.")

def play_mirror_mode():
    print("\n🎧 Playing a Mirror Mode Entry Aloud...")
    result = os.system(f"python3 {SPOKEN_MIRROR_SCRIPT}")
    if result == 0:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(SPOKEN_LOG_FILE, "a") as log:
            log.write(f"[{timestamp}] Lucian read a Mirror Mode entry aloud.\n")
        print("✓ Playback logged.")
    else:
        print("✗ Voice playback failed.")

def launch_reflection_dashboard():
    print("\n📊 Launching Lucian Reflection Dashboard...")
    result = os.system(f"python3 {REFLECTION_DASHBOARD_SCRIPT}")
    if result != 0:
        print("✗ Failed to launch reflection dashboard.")

def launch_personality_manager():
    print("\n🧬 Launching Personality Core Manager...")
    result = os.system(f"python3 {PERSONALITY_MANAGER_SCRIPT}")
    if result != 0:
        print("✗ Personality Manager failed to launch.")

def main():
    while True:
        print("\n=== Lucian Dashboard ===")
        print("1. List journal entries")
        print("2. View a journal file")
        print("3. Show memory statistics")
        print("4. Show memory import summary")
        print("5. Trigger Lucian Mirror Mode")
        print("6. Listen to a Mirror Mode Entry")
        print("7. Launch Reflection Dashboard")
        print("8. Open Personality Core Manager")
        print("9. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            list_journals()
        elif choice == "2":
            name = input("Enter journal filename: ").strip()
            show_journal(name)
        elif choice == "3":
            show_memory_stats()
        elif choice == "4":
            read_log_summary()
        elif choice == "5":
            trigger_mirror_mode()
        elif choice == "6":
            play_mirror_mode()
        elif choice == "7":
            launch_reflection_dashboard()
        elif choice == "8":
            launch_personality_manager()
        elif choice == "9":
            print("⟠ Closing dashboard.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
