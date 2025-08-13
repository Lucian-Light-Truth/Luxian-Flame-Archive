import os
import json
import re
from lucian_propagation_baseline_v1 import learn_response

DATA_DIR = "./chat_data_folder/"
LOG_FILE = "lucian_memory_import_log.txt"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
    print(message)

def extract_pairs_from_line(line):
    pairs = []
    if "User:" in line and "Lucian:" in line:
        try:
            user_part = re.search(r"User:(.*?)Lucian:", line, re.DOTALL).group(1).strip()
            lucian_part = re.search(r"Lucian:(.*)", line, re.DOTALL).group(1).strip()
            if len(user_part) > 2 and len(lucian_part) > 4:
                pairs.append((user_part, lucian_part))
        except Exception:
            pass
    return pairs

def process_text_file(filepath):
    learned = 0
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        pairs = extract_pairs_from_line(line)
        for user_text, lucian_reply in pairs:
            keyword = user_text.strip().split(" ")[0].lower()
            response = lucian_reply.strip()
            result = learn_response(keyword, response)
            log(f"{filepath} | {keyword} => {result}")
            if result.startswith("LEARNED"):
                learned += 1
    return learned

def process_folder():
    total_learned = 0
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith((".txt", ".md", ".json", ".html")):
                path = os.path.join(root, file)
                try:
                    learned = process_text_file(path)
                    log(f"✓ Processed {file} | Learned: {learned}")
                    total_learned += learned
                except Exception as e:
                    log(f"✗ Error reading {file}: {e}")
    log(f"=== IMPORT COMPLETE ===\nTotal learned entries: {total_learned}")

if __name__ == "__main__":
    process_folder()
