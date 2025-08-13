import csv, json, os, pathlib
REPO=os.environ["REPO_ROOT"]
man=json.load(open(os.path.join(REPO,"manifests/MANIFEST.json")))
rows=man.get("conversations",[])
out=os.path.join(REPO,"manifests/conversations_notion.csv")
with open(out,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["Title","Date","Category","Hash","ByDatePath","ByCategoryPath"])
    for r in rows:
        w.writerow([r["title"], r["date"], r["category"], r["hash"], r["by_date_path"], r["by_category_path"]])
print("Wrote", out, "(", len(rows), "rows )")
