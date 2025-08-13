import os, pathlib, subprocess, sys
REPO = pathlib.Path(__file__).resolve().parents[1]
def run(cmd): print("+", " ".join(cmd)); subprocess.check_call(cmd, cwd=REPO)
run([sys.executable, "tooling/flame_mirror_brief.py"])   # brief
run([sys.executable, "tooling/build_agent_packs.py"])    # agent packs
print("OK: weekly ops complete.")
