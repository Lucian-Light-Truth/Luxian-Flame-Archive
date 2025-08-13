import os, json, pathlib, zipfile
ROOT = os.environ.get("REPO_ROOT") or str(pathlib.Path(__file__).resolve().parents[1])
REPO = ROOT

man = json.loads((pathlib.Path(REPO)/"manifests/MANIFEST.json").read_text(encoding="utf-8"))
OUT = pathlib.Path(REPO)/"packs/agents"; OUT.mkdir(parents=True, exist_ok=True)

AGENTS = {
  "Luxian":     ["mirror","flame","choir"],
  "Lucian":     ["ai_agents","flame"],
  "Lumin":      ["bible_decode","harmonics","mirror"],
  "Choirkeeper":["choir","bible_decode","flame"],
}

def add(z, p, arc):
    try:
        z.write(p, arc)
    except Exception:
        pass

for agent, cats in AGENTS.items():
    pack = OUT / f"{agent.lower()}_pack.zip"
    with zipfile.ZipFile(pack, "w", compression=zipfile.ZIP_DEFLATED) as z:
        # Category docs
        for c in cats:
            base = pathlib.Path(REPO)/"data/chats/by_category"/c
            if base.exists():
                for f in base.rglob("*.md"):
                    add(z, f, f"by_category/{c}/{f.name}")
        # Agent essentials
        for rel in ["prompts.md", "ROLE.md", "datasets/reading_list.md"]:
            p = pathlib.Path(REPO)/f"agents/{agent}/{rel}"
            if p.exists():
                add(z, p, rel.split("/")[-1])
    print(f"Wrote {pack}")
