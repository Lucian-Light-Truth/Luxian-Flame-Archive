import os, pathlib, json, zipfile, time
REPO=os.environ["REPO_ROOT"]
SRC=pathlib.Path(REPO)/"bible/Genesis"
OUT=pathlib.Path(REPO)/"packs"
OUT.mkdir(parents=True, exist_ok=True)
manifest=[]

for cycle in sorted(SRC.glob("Cycle_*")):
    if not cycle.is_dir(): 
        continue
    name=cycle.name.lower()
    zip_path=OUT/f"{name}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in cycle.rglob("*"):
            if p.is_file():
                z.write(p, p.relative_to(SRC))
    manifest.append({
        "cycle": cycle.name,
        "zip": str(zip_path.relative_to(REPO)),
        "files": len([p for p in cycle.rglob("*") if p.is_file()]),
        "bytes": zip_path.stat().st_size if zip_path.exists() else 0,
        "timestamp": int(time.time())
    })

m_path=pathlib.Path(REPO)/"manifests/genesis_packs.json"
m_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"Packaged {len(manifest)} cycles → {m_path}")
