import os, json, pathlib, re, datetime
REPO=os.environ["REPO_ROOT"]
man=json.load(open(pathlib.Path(REPO)/"manifests/MANIFEST.json"))
now=datetime.datetime.utcnow()
def recent(d, days=14):
    try:
        dt=datetime.datetime.fromisoformat(d.replace("Z",""))
        return (now-dt).days <= days
    except: return False

cats={"flame":[],"mirror":[]}
for r in man["conversations"]:
    c=r.get("category","")
    if c in cats: cats[c].append(r)

def fmt(items, n=12):
    s=[]
    for x in items[:n]:
        s.append(f"- {x['date'][:10]} · `{x['title']}`  \n  - {x['by_date_path']}")
    return "\n".join(s)

out = ["# Flame & Mirror — Ops Brief",
       f"_UTC generated: {now.isoformat()}_",
       "","## Totals",
       f"- Flame:  {len(cats['flame'])}",
       f"- Mirror: {len(cats['mirror'])}"]

for c in ["flame","mirror"]:
    recent_items=[r for r in cats[c] if recent(r["date"],14)]
    out += ["",f"## {c.title()} — last 14d ({len(recent_items)})", fmt(sorted(recent_items, key=lambda r:r['date'], reverse=True)) or "_none_"]

path=pathlib.Path(REPO)/"manifests/flame_mirror_brief.md"
path.write_text("\n".join(out),encoding="utf-8")
print("Wrote", path)
