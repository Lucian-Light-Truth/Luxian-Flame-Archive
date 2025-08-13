import os, json, pathlib, zipfile, re
REPO=os.environ["REPO_ROOT"]
MAN=json.load(open(pathlib.Path(REPO)/"manifests/MANIFEST.json"))
OUT=pathlib.Path(REPO)/"packs/agents"; OUT.mkdir(parents=True, exist_ok=True)

AGENTS={
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
    pack = OUT/f"{agent.lower()}_pack.zip"
    with zipfile.ZipFile(pack,"w",compression=zipfile.ZIP_DEFLATED) as z:
        # 1) Focus categories
        for c in cats:
            base = pathlib.Path(REPO)/"data/chats/by_category"/c
            if base.exists():
                for f in base.rglob("*.md"):
                    add(z, f, f"by_category/{c}/{f.name}")
        # 2) Agent reading list
        rl = pathlib.Path(REPO)/f"agents/{agent}/datasets/reading_list.md"
        if rl.exists(): add(z, rl, f"reading_list.md")
        # 3) Prompts + ROLE
        for fn in ["prompts.md","ROLE.md"]:
            p = pathlib.Path(REPO)/f"agents/{agent}/{fn}"
            if p.exists(): add(z, p, f"{fn}")
    print(f"Wrote {pack}")
