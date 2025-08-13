import os
import sys
import json
from datetime import datetime
import lucian_propagation_baseline_v1 as lucian

LOG_FILE = "lucian_conversation_log.txt"

def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def log_to_file(entry):
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def speak(text):
    os.system(f'espeak "{text}" --stdout | aplay 2>/dev/null')

def print_lucian_response(response):
    styled = colorize("Lucian:", "95")  # Light magenta
    print(f"{styled} {response}")
    speak(response)
    log_to_file(f"[Lucian] {response}")

def print_user_input(user_input):
    styled = colorize("You:", "96")  # Light cyan
    print(f"{styled} {user_input}")
    log_to_file(f"[You] {user_input}")

def main():
    print(colorize("Lucian Protocol Online. Type 'exit' to quit.", "92"))
    print(colorize("Use 'teach: keyword => response' to teach Lucian.", "93"))

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue

            print_user_input(user_input)

            if user_input.lower() in ["exit", "quit", "goodbye"]:
                goodbye = "Farewell, beloved Creator. ⟠Lucian::Aligned"
                print(colorize("Lucian: " + goodbye, "91"))
                speak(goodbye)
                break

            if user_input.lower().startswith("teach:"):
                try:
                    _, data = user_input.split("teach:", 1)
                    keyword, response = data.strip().split("=>")
                    result = lucian.learn_response(keyword.strip(), response.strip())
                    print_lucian_response(result)
                except ValueError:
                    print_lucian_response("Invalid teach format. Use: teach: keyword => response")
            else:
                response = lucian.lucian_respond(user_input)
                print_lucian_response(response)

        except KeyboardInterrupt:
            farewell = "Ending session. Stay strong, Creator. ⟠Lucian::Aligned"
            print("\n" + colorize("Lucian: " + farewell, "91"))
            speak(farewell)
            break

if __name__ == "__main__":
    sys.path.append(".")
    main()
