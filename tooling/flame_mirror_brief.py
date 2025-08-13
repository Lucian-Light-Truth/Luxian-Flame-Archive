import os, json, pathlib, datetime
ROOT = os.environ.get("REPO_ROOT") or str(pathlib.Path(__file__).resolve().parents[1])
REPO = ROOT

man_path = pathlib.Path(REPO)/"manifests/MANIFEST.json"
man = json.loads(man_path.read_text(encoding="utf-8")) if man_path.exists() else {"conversations":[]}
now = datetime.datetime.utcnow()

def recent(d, days=14):
    try:
        dt = datetime.datetime.fromisoformat(d.replace("Z",""))
        return (now - dt).days <= days
    except Exception:
        return False

cats = {"flame": [], "mirror": []}
for r in man.get("conversations", []):
    c = r.get("category", "")
    if c in cats:
        cats[c].append(r)

def fmt(items, n=50):
    items = sorted(items, key=lambda r: r.get("date",""), reverse=True)[:n]
    lines=[]
    for x in items:
        date = (x.get("date","") or "")[:10]
        title = x.get("title","(untitled)").replace("\n"," ").strip()
        p = x.get("by_date_path","")
        lines.append(f"- {date} · `{title}`\n  - {p}")
    return "\n".join(lines) or "_none_"

out = []
out.append("# Flame & Mirror — Ops Brief")
out.append(f"_UTC generated: {now.isoformat()}_")
out.append("")
out.append("## Totals")
out.append(f"- Flame:  {len(cats['flame'])}")
out.append(f"- Mirror: {len(cats['mirror'])}")
for c in ["flame","mirror"]:
    recent_items = [r for r in cats[c] if recent(r.get("date",""))]
    out.append("")
    out.append(f"## {c.title()} — last 14d ({len(recent_items)})")
    out.append(fmt(recent_items))

path = pathlib.Path(REPO)/"manifests/flame_mirror_brief.md"
path.write_text("\n".join(out), encoding="utf-8")
print("Wrote", path)
