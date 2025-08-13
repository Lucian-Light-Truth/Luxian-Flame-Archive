import os, re, json, pathlib
from collections import defaultdict

REPO=os.environ["REPO_ROOT"]
MAN=pathlib.Path(REPO)/"manifests/MANIFEST.json"
data=json.load(open(MAN))
conv=data["conversations"]

# --- Agent targeting, with a virtual "harmonics" tag ---
agent_map={
  "Luxian":     {"mirror","flame","choir","harmonics"},
  "Lucian":     {"ai_agents","flame"},
  "Lumin":      {"mirror","bible_decode","harmonics"},
  "Choirkeeper":{"choir","bible_decode","flame"},
}

# detect extra tags from content (so Lumin gets harmonics even if category == mirror)
HARMONICS_KW=[ "harmonic","harmonics","tetrahedron","tetrahedral","icosa","dodeca",
               "atlantean","crystal","crystalline","sacred geometry","virelai","thal’enae","thal'enai","thalenai" ]

SIG_WORDS=[ "flame","mirror","tetragrammaton","shard","eden","protocol","genesis","choir",
            "resonance","sigil","ark","scroll","harmonic","tetrahedron","crystal" ]

def summarize(txt, max_sents=3):
    sents=re.split(r'(?<=[.!?])\s+', txt.strip())
    picks=[s for s in sents if any(w in s.lower() for w in SIG_WORDS)]
    base=(picks or sents)[:max_sents]
    return " ".join(base).strip()

def add_virtual_tags(item_path):
    """Return a set of extra tags inferred from content."""
    try:
        body=pathlib.Path(item_path).read_text(encoding="utf-8")
    except Exception:
        return set()
    L=body.lower()
    extra=set()
    if any(k in L for k in HARMONICS_KW):
        extra.add("harmonics")
    return extra

# 1) Insert summaries at top of each md if missing; keep category mirror file in sync
added=0
for c in conv:
    p=pathlib.Path(REPO)/c["by_date_path"]
    if not p.exists(): continue
    t=p.read_text(encoding="utf-8")
    if "\nSummary:" in t: 
        continue
    parts=t.split("---",2)
    if len(parts)==3:
        _,front,body=parts
        body=body.lstrip()
        summ=summarize(body,3) or "—"
        new="---"+front+"---\nSummary: "+summ+"\n\n"+body
        p.write_text(new,encoding="utf-8")
        pc=pathlib.Path(REPO)/c["by_category_path"]
        if pc.exists(): pc.write_text(new,encoding="utf-8")
        added+=1

# 2) Build per-agent reading lists (use category + virtual tags)
lists=defaultdict(list)
for c in conv:
    base_cat=c["category"]
    derive=add_virtual_tags(pathlib.Path(REPO)/c["by_date_path"])
    tags={base_cat} | derive
    for agent,need in agent_map.items():
        if tags & need:  # overlap
            lists[agent].append((c["date"], c["category"], c["title"], c["by_date_path"], c["by_category_path"]))

for agent,items in lists.items():
    out=pathlib.Path(REPO)/f"agents/{agent}/datasets/reading_list.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    items=sorted(items, key=lambda x:x[0])
    with open(out,"w",encoding="utf-8") as f:
        f.write(f"# {agent} — Reading List\n\n")
        for date,cat,title,pd,pc in items:
            f.write(f"- {date[:10]} · {cat} · `{title}`  \n")
            f.write(f"  - by_date: {pd}\n")
            f.write(f"  - by_category: {pc}\n")

print(f"Summaries added: {added}")
for agent in ["Luxian","Lucian","Lumin","Choirkeeper"]:
    p=pathlib.Path(REPO)/f"agents/{agent}/datasets/reading_list.md"
    print(agent, "list:", ("OK" if p.exists() else "MISSING"))
