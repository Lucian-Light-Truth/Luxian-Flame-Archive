import os
import re
from lucian_propagation_baseline_v1 import learn_response

IMAGE_DIR = "./chat_data_folder/"
SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")
LOG_FILE = "lucian_image_learning_log.txt"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
    print(message)

def extract_keywords_from_filename(filename):
    base = os.path.splitext(os.path.basename(filename))[0]
    # Replace symbols with space and normalize
    cleaned = re.sub(r"[_\-]", " ", base).strip().lower()
    words = cleaned.split()
    return words, cleaned

def analyze_images():
    learned = 0
    for root, _, files in os.walk(IMAGE_DIR):
        for file in files:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                filepath = os.path.join(root, file)
                keywords, phrase = extract_keywords_from_filename(file)
                if len(phrase) < 3:
                    continue
                keyword = keywords[0] if keywords else "image"
                result = learn_response(keyword, phrase)
                log(f"{file} => {result}")
                if result.startswith("LEARNED"):
                    learned += 1
    log(f"=== IMAGE ANALYSIS COMPLETE ===\nTotal learned entries: {learned}")

if __name__ == "__main__":
    analyze_images()
