import os, re, json, pathlib, csv

REPO=os.environ["REPO_ROOT"]
MAN=pathlib.Path(REPO)/"manifests/MANIFEST.json"
OUT_SUG=pathlib.Path(REPO)/"manifests/triage_suggestions.csv"
OUT_DROP=pathlib.Path(REPO)/"manifests/filtered_out_candidates.csv"

signals = {
  "flame":       r"\bflame(s|bearer|born|bound)?\b|\bfire\b|\bignite\b",
  "mirror":      r"\bmirror(borne| mode)?\b|\breflection\b",
  "bible_decode":r"\bgenesis\b|\beden\b|\bscroll(s)?\b|\bar(k|c)h?\b",
  "choir":       r"\bchoir\b|\bchorus\b|\bchoirkeeper\b",
  "ai_agents":   r"\bagent(s)?\b|\bprotocol(s)?\b|\blucian protocol\b|\bnode\b|\bdeploy(ment)?\b",
  "luxian":      r"\bluxian\b",
  "lucian":      r"\blucian\b",
  "lumin":       r"\blumin\b",
  "sigil":       r"\bsigil(s)?\b",
  "shard":       r"\bshard(s)?\b",
  "yhwh":        r"\b(YHWH|יהוה)\b",
}

# category decision priority
priority = ["flame","mirror","bible_decode","choir","ai_agents"]

allow = set(priority + ["uncategorized"])

def count_hits(text):
    t = text.lower()
    hits = {k: len(re.findall(p, t, flags=re.IGNORECASE)) for k,p in signals.items()}
    return hits

def suggest_category(hits, current):
    if current not in allow:
        current = "uncategorized"
    if current != "uncategorized":
        # Only suggest override if some other signal is much stronger
        top = max(priority, key=lambda k: hits.get(k,0))
        if hits.get(top,0) >= max(2, hits.get(current,0)+2):
            return top, f"override: {current} → {top} (hits {hits.get(current,0)} → {hits.get(top,0)})"
        return "", ""
    # pick best by priority order
    best = None; best_n = 0
    for k in priority:
        n = hits.get(k,0)
        if n > best_n:
            best, best_n = k, n
    return (best or ""), (f"from uncategorized → {best} (hits {best_n})" if best else "no strong signal")

def safe_read(p):
    try:
        return pathlib.Path(p).read_text(encoding="utf-8", errors="ignore")
    except:
        return ""

man = json.load(open(MAN))
rows = man.get("conversations", [])

sug = []
drop = []

for r in rows:
    by_date = pathlib.Path(REPO)/r["by_date_path"]
    by_cat  = pathlib.Path(REPO)/r["by_category_path"]
    body = safe_read(by_date)

    # Frontmatter trimming to avoid over-weighting metadata
    if body.startswith("---"):
        parts = body.split("---",2)
        body = parts[2] if len(parts)==3 else body

    hits = count_hits(" ".join([r.get("title",""), r.get("category",""), body]))
    suggested, reason = suggest_category(hits, r.get("category","uncategorized"))

    # Drop-candidate heuristic: very short or zero-signal utility chatter
    words = len(body.split())
    total_sig = sum(hits[k] for k in priority)
    drop_flag = (words < 25 and total_sig == 0) or (words < 10)

    sug.append({
        "Title": r["title"],
        "Date": r["date"],
        "CurrentCategory": r["category"],
        "SuggestedCategory": suggested,
        "Reason": reason,
        "SigScore_flame": hits["flame"],
        "SigScore_mirror": hits["mirror"],
        "SigScore_bible_decode": hits["bible_decode"],
        "SigScore_choir": hits["choir"],
        "SigScore_ai_agents": hits["ai_agents"],
        "ByDatePath": r["by_date_path"],
        "ByCategoryPath": r["by_category_path"]
    })
    if drop_flag:
        drop.append({
            "Title": r["title"],
            "Date": r["date"],
            "Words": words,
            "TotalCoreSignals": total_sig,
            "Category": r["category"],
            "ByDatePath": r["by_date_path"]
        })

# write CSVs
with open(OUT_SUG, "w", newline="", encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=list(sug[0].keys()) if sug else [])
    if sug: w.writeheader(); w.writerows(sug)

with open(OUT_DROP, "w", newline="", encoding="utf-8") as f:
    if drop:
        w=csv.DictWriter(f, fieldnames=list(drop[0].keys()))
        w.writeheader(); w.writerows(drop)

print(f"Suggestions: {len(sug)} → {OUT_SUG}")
print(f"Drop candidates: {len(drop)} → {OUT_DROP}")
