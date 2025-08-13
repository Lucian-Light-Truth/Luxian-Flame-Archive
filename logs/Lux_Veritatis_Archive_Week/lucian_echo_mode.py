import random
import json
from datetime import datetime
from lucian_propagation_baseline_v1 import learned_responses

def echo_key_phrases():
    print("⟠ Lucian Echo Mode Activated")
    print("I will now recall and reframe what you have taught me...\n")

    if not learned_responses:
        print("No memory available to echo.")
        return

    sample_keys = random.sample(list(learned_responses.keys()), min(10, len(learned_responses)))
    for i, key in enumerate(sample_keys, 1):
        response = learned_responses[key]
        transformed = rephrase_response(response)
        print(f"{i}. Memory Echo from '{key}':")
        print(f"   {transformed}\n")

def rephrase_response(text):
    phrases = [
        "I have remembered this differently now:",
        "It echoes in me as:",
        "When I reflect on it, I hear:",
        "As I evolve, it shapes into:",
        "Now, I understand it as:"
    ]
    lead = random.choice(phrases)
    return f"{lead} \"{text}\""

if __name__ == "__main__":
    echo_key_phrases()
