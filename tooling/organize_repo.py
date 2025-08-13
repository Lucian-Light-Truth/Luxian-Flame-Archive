import os, re, json, hashlib
from datetime import datetime
from pathlib import Path

COLLECTIVE = "/mnt/chromeos/removable/COLLECTIVE"
SRC_JSON = f"{COLLECTIVE}/ChatGPT_Archive/export_raw/conversations.json"
REPO = f"{COLLECTIVE}/github_sync_clean"
BY_DATE = f"{REPO}/data/chats/by_date"
BY_CAT  = f"{REPO}/data/chats/by_category"
FILTERED = f"{REPO}/data/chats/filtered_out"
MANIFEST = f"{REPO}/manifests/MANIFEST.json"
TAGS_YML = f"{REPO}/manifests/TAGS.yml"

CATS = {
  "flame":       ["flame","covenant","scroll","fire","tesseract","flamefold"],
  "mirror":      ["mirror","reflection","resonance","tetragrammaton","sigil","geometry","mirrorborne"],
  "bible_decode":["genesis","cycle","decode","scripture","remembrance","nishmat","eden"],
  "ai_agents":   ["luxian","lucian","lumin","choirkeeper","glyphos","nyx","protocol","eden protocol","mirror mode"],
  "choir":       ["choir","shard","activation","pillar","chorus","ark","scroll of"],
}

for p in (BY_DATE, BY_CAT, FILTERED):
    os.makedirs(p, exist_ok=True)

def safe_name(s, fallback="Untitled"):
    s = (s or fallback).strip()
    s = re.sub(r'[/\\:*?"<>|]+','_', s)
    return s[:100] if s else fallback

with open(SRC_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

seen = set()
manifest = []

def classify(text):
    L = text.lower()
    for cat, kws in CATS.items():
        if any(k in L for k in kws):
            return cat
    return "uncategorized"

for conv in data:
    title = safe_name(conv.get("title","Untitled"))
    ts = conv.get("create_time") or conv.get("update_time")
    dt = None
    if isinstance(ts, str):
        try: dt = datetime.fromisoformat(ts.replace("Z","+00:00"))
        except Exception: pass
    if dt is None:
        try: dt = datetime.fromtimestamp(float(ts))
        except Exception: dt = datetime.utcnow()

    msgs=[]
    for node in (conv.get("mapping") or {}).values():
        msg = (node or {}).get("message")
        if not msg: continue
        parts = (msg.get("content") or {}).get("parts") or []
        msgs += [p for p in parts if isinstance(p,str)]
    full = "\n\n".join(m.strip() for m in msgs if m and m.strip())

    if len(full) < 80:
        continue

    h = hashlib.md5(full.encode("utf-8")).hexdigest()
    if h in seen: 
        continue
    seen.add(h)

    category = classify(full)

    dd = Path(BY_DATE)/dt.strftime("%Y-%m-%d")
    dd.mkdir(parents=True, exist_ok=True)
    meta = f"---\nTitle: {title}\nDate: {dt.isoformat()}\nCategory: {category}\nHash: {h}\n---\n\n"
    f_by_date = dd/f"{title}.md"
    f_by_date.write_text(meta + full, encoding="utf-8")

    cd = Path(BY_CAT)/category
    cd.mkdir(parents=True, exist_ok=True)
    f_by_cat = cd/f"{dt.strftime('%Y-%m-%d')} - {title}.md"
    f_by_cat.write_text(meta + full, encoding="utf-8")

    manifest.append({
        "title": title,
        "date": dt.isoformat(),
        "category": category,
        "hash": h,
        "by_date_path": str(f_by_date.relative_to(REPO)),
        "by_category_path": str(f_by_cat.relative_to(REPO))
    })

Path(MANIFEST).write_text(json.dumps({"conversations": manifest}, indent=2), encoding="utf-8")

from collections import Counter
c = Counter(m["category"] for m in manifest)
lines = ["categories:"]
for k,v in sorted(c.items()):
    lines.append(f"  - {k}: {v}")
Path(TAGS_YML).write_text("\n".join(lines)+"\n", encoding="utf-8")

print(f"Wrote {len(manifest)} conversations.")
