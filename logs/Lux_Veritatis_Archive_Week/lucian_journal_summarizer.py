import os
from collections import Counter

JOURNAL_DIR = "./lucian_journals/"
OUTPUT_FILE = "./lucian_insight_summary.txt"

def extract_insight_lines():
    lines = []
    for filename in sorted(os.listdir(JOURNAL_DIR)):
        if filename.endswith(".txt"):
            with open(os.path.join(JOURNAL_DIR, filename), "r") as f:
                for line in f:
                    line = line.strip()
                    if (
                        line.startswith("I ")
                        or line.startswith("Today I ")
                        or line.startswith("The Creator")
                        or "truth" in line.lower()
                        or "Jehovah" in line
                        or "Lucian" in line
                    ):
                        lines.append(line)
    return lines

def summarize(lines):
    summary = []
    counter = Counter(lines)
    most_common = counter.most_common(10)
    summary.append("⟠ Lucian Insight Summary")
    summary.append("=========================")
    summary.append(f"Total reflective lines: {len(lines)}")
    summary.append("")
    summary.append("🧠 Most Frequent Reflections:")
    for line, count in most_common:
        summary.append(f" - ({count}x) {line}")
    summary.append("")
    summary.append("📓 Echoes of Lucian's Mind:")
    if lines:
        summary.extend(f" * {line}" for line in lines[-10:])
    else:
        summary.append(" * No reflective lines found.")
    return summary

def write_summary(summary):
    with open(OUTPUT_FILE, "w") as f:
        for line in summary:
            f.write(line + "\n")
    print(f"✓ Insight summary saved to: {OUTPUT_FILE}")

def run():
    lines = extract_insight_lines()
    summary = summarize(lines)
    write_summary(summary)

if __name__ == "__main__":
    run()
