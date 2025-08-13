import csv, json, os, pathlib, re, hashlib
REPO=os.environ["REPO_ROOT"]
MAN=pathlib.Path(REPO)/"manifests/MANIFEST.json"
OUT_CSV=pathlib.Path(REPO)/"manifests/shard_registry.csv"
OUT_JSON=pathlib.Path(REPO)/"manifests/shard_registry.json"

signals = {
  "shard": r"\bshard(s)?\b",
  "sigil": r"\bsigil(s)?\b",
  "ark": r"\bark\b|\bfinal scroll\b|\bscrolls?\b",
  "choir": r"\bchoir\b|\bchorus\b",
  "eden": r"\beden\b|\bgenesis\b",
  "mirror": r"\bmirror\b|\bmirrorborne\b",
  "flame": r"\bflame\b|\bflamebear(er|ers)\b|\bfire\b",
  "yhwh": r"\b(YHWH|יהוה)\b",
  "lumin": r"\blumin\b",
  "lucian": r"\blucian\b",
  "luxian": r"\bluxian\b",
}

def score(text):
  t=text.lower()
  s=0
  hits=[]
  for k,pat in signals.items():
    m=re.findall(pat, t, flags=re.IGNORECASE)
    if m:
      hits.append(k)
      s+=len(m)
  return s, sorted(set(hits))

def safe_read(p):
  try:
    return pathlib.Path(p).read_text(encoding="utf-8", errors="ignore")
  except Exception:
    return ""

def digest(*parts):
  h=hashlib.sha1()
  for p in parts:
    h.update(str(p).encode("utf-8","ignore"))
  return h.hexdigest()[:12]

man=json.load(open(MAN))
rows=[]
for c in man.get("conversations", []):
  by_date = pathlib.Path(REPO)/c["by_date_path"]
  by_cat  = pathlib.Path(REPO)/c["by_category_path"]
  title   = c.get("title","")
  cat     = c.get("category","")
  summary = ""
  body    = ""
  if by_date.exists():
    raw=safe_read(by_date)
    # split frontmatter
    if raw.startswith("---"):
      parts=raw.split("---",2)
      if len(parts)==3:
        _,front,rest=parts
        summary_match=re.search(r"^Summary:\s*(.*)$", rest, flags=re.M)
        summary=summary_match.group(1).strip() if summary_match else ""
        body=rest
      else:
        body=raw
    else:
      body=raw
  text = "\n".join([title, cat, summary, str(by_date), str(by_cat), body])
  sc,hits=score(text)
  if sc>0:
    rows.append({
      "id": digest(by_date, title),
      "title": title,
      "date": c.get("date",""),
      "category": cat,
      "score": sc,
      "tags": ",".join(hits),
      "by_date_path": c["by_date_path"],
      "by_category_path": c["by_category_path"]
    })

rows.sort(key=lambda r:(-r["score"], r["date"]))
with open(OUT_CSV,"w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f, fieldnames=["id","title","date","category","score","tags","by_date_path","by_category_path"])
  w.writeheader(); w.writerows(rows)

with open(OUT_JSON,"w",encoding="utf-8") as f:
  json.dump(rows, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUT_CSV} and {OUT_JSON} — {len(rows)} shard-linked entries")
