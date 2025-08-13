import os
import time
import re

MIRROR_DIR = "./lucian_mirror_mode/"

def list_entries():
    entries = sorted([
        f for f in os.listdir(MIRROR_DIR)
        if f.startswith("mirror_mode_") and f.endswith(".txt")
    ])
    return entries

def clean_text(text):
    text = re.sub(r"[⟠🪞💬🔥💙]", "", text)
    text = text.replace("—", "-").replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return text.strip()

def speak(text, engine="espeak-ng"):
    safe_text = clean_text(text)
    os.system(f'{engine} "{safe_text}" 2>/dev/null')

def read_and_speak_file(path, engine="espeak-ng"):
    with open(path, "r") as f:
        lines = f.readlines()

    print("\n🎙️ Reading aloud with Lucian:")
    for line in lines:
        line = line.strip()
        if not line:
            time.sleep(1)
            continue
        print(f"> {line}")
        speak(line, engine)
        time.sleep(0.5)

def run():
    entries = list_entries()
    if not entries:
        print("No mirror mode entries found.")
        return

    print("\n🪞 Mirror Mode Entries:")
    for i, name in enumerate(entries):
        print(f"{i+1}. {name}")
    choice = input("Select an entry to read aloud: ").strip()

    try:
        index = int(choice) - 1
        file_path = os.path.join(MIRROR_DIR, entries[index])
        read_and_speak_file(file_path)
    except:
        print("Invalid selection.")

if __name__ == "__main__":
    run()
