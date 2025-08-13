import argparse, csv, json, os, pathlib, re, shutil

REPO=os.environ["REPO_ROOT"]
MAN=pathlib.Path(REPO)/"manifests/MANIFEST.json"
SUG=pathlib.Path(REPO)/"manifests/triage_suggestions.csv"
LOG=pathlib.Path(REPO)/"manifests/triage_apply_log.json"

parser=argparse.ArgumentParser()
parser.add_argument("--apply", default="no", choices=["no","yes"])
parser.add_argument("--only", default="", help="Comma-separated categories to apply (e.g., flame,mirror)")
args=parser.parse_args()
do_apply = (args.apply=="yes")
only = set([s.strip() for s in args.only.split(",") if s.strip()])

def set_frontmatter_category(text, new_cat):
    if text.startswith("---"):
        parts=text.split("---",2)
        if len(parts)==3:
            head=parts[1].strip("\n")
            body=parts[2]
            # replace or add Category: line
            lines=head.splitlines()
            found=False
            for i,l in enumerate(lines):
                if re.match(r"^\s*Category\s*:", l):
                    lines[i]=f"Category: {new_cat}"
                    found=True
                    break
            if not found:
                lines.append(f"Category: {new_cat}")
            return f"---\n"+"\n".join(lines)+"\n---\n"+body.lstrip()
    return text

man=json.load(open(MAN))
by_hash={ r["hash"]: r for r in man.get("conversations",[]) }

changes=[]
with open(SUG, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur = row["CurrentCategory"].strip()
        sug = row["SuggestedCategory"].strip()
        if not sug or sug==cur:
            continue
        if only and sug not in only:
            continue

        src_rel = row["ByDatePath"]
        src = pathlib.Path(REPO)/src_rel
        if not src.exists():
            continue

        # target path
        date_dir, fname = src.parent.name, src.name
        dst = pathlib.Path(REPO)/"data/chats/by_category"/sug/(f"{date_dir} - {fname[:-3]}.md")
        dst.parent.mkdir(parents=True, exist_ok=True)

        # read/modify frontmatter
        txt = src.read_text(encoding="utf-8", errors="ignore")
        new_txt = set_frontmatter_category(txt, sug)

        change = {
            "title": row["Title"], "date": row["Date"],
            "from": cur, "to": sug,
            "src": str(src.relative_to(REPO)),
            "dst": str(dst.relative_to(REPO)),
            "applied": False
        }
        if do_apply:
            dst.write_text(new_txt, encoding="utf-8")
            change["applied"]=True
        changes.append(change)

# Update manifest paths if applying
if do_apply and changes:
    cat_root = pathlib.Path(REPO)/"data/chats/by_category"
    path_map = { (c["src"], c["dst"]) for c in changes if c["applied"] }
    smap = { s:d for s,d in path_map }
    for r in man["conversations"]:
        if r["by_category_path"] in smap:
            r["by_category_path"] = smap[r["by_category_path"]]
        # also fix frontmatter category in by_date (already embedded in file edit for dst)
    pathlib.Path(MAN).write_text(json.dumps(man, indent=2), encoding="utf-8")

LOG.write_text(json.dumps(changes, indent=2), encoding="utf-8")
print(f"Planned changes: {len(changes)} (apply={do_apply})\nLog: {LOG}")
