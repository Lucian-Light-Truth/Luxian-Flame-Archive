import os, pathlib, json, hashlib, sys, argparse, re, subprocess, time

REPO = os.environ.get("REPO_ROOT", os.getcwd())
OUT  = pathlib.Path(REPO)/"manifests"
OUT.mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("--apply", default="no", choices=["no","yes"], help="Actually remove items")
args = parser.parse_args()
APPLY = (args.apply == "yes")

zero_files = []
empty_dirs = []
junk_files = []
broken_links = []
non_utf8_files = []
large_non_lfs = []
secrets_hits = []

JUNK_PATTERNS = (".DS_Store","Thumbs.db")
SECRET_REGEX  = re.compile(r'(sk-[A-Za-z0-9_\-]{20,}|github_pat_[A-Za-z0-9_\-]{20,}|ghp_[A-Za-z0-9_\-]{20,})')

# Get LFS tracked patterns
def lfs_tracked_globs():
    try:
        gitattributes = pathlib.Path(REPO)/".gitattributes"
        globs=[]
        if gitattributes.exists():
            for line in gitattributes.read_text(errors="ignore").splitlines():
                if "filter=lfs" in line:
                    globs.append(line.split()[0].strip('"'))
        return globs
    except:
        return []

def matches_any_glob(path: pathlib.Path, globs):
    from fnmatch import fnmatch
    rel = str(path.relative_to(REPO))
    return any(fnmatch(rel, g) for g in globs)

lfs_globs = lfs_tracked_globs()

# Walk repo
for root, dirs, files in os.walk(REPO):
    # skip .git
    if "/.git" in root or root.endswith("/.git"):
        continue
    p_root = pathlib.Path(root)

    # Files
    for fn in files:
        p = p_root / fn
        try:
            # broken symlinks
            if p.is_symlink() and not p.exists():
                broken_links.append(str(p.relative_to(REPO)))
                continue

            # junk files
            if fn in JUNK_PATTERNS or fn.startswith("._"):
                junk_files.append(str(p.relative_to(REPO)))

            # zero-byte
            if p.stat().st_size == 0:
                zero_files.append(str(p.relative_to(REPO)))

            # non-utf8 (best-effort)
            try:
                if p.suffix.lower() in (".md",".txt",".json",".py",".yml",".yaml",".toml",".csv"):
                    _ = p.read_text(encoding="utf-8")
            except Exception:
                non_utf8_files.append(str(p.relative_to(REPO)))

            # secrets quick scan (only texty)
            try:
                if p.suffix.lower() in (".md",".txt",".json",".py",".yml",".yaml",".toml",".env"):
                    txt = p.read_text(errors="ignore")
                    if SECRET_REGEX.search(txt):
                        secrets_hits.append(str(p.relative_to(REPO)))
            except Exception:
                pass

            # large non-LFS
            if p.stat().st_size > 5 * 1024 * 1024:  # >5MB
                if not matches_any_glob(p, lfs_globs):
                    large_non_lfs.append({
                        "path": str(p.relative_to(REPO)),
                        "size_bytes": p.stat().st_size
                    })

        except FileNotFoundError:
            # race with symlinks
            broken_links.append(str(p.relative_to(REPO)))
            continue

# empty dirs (collect after scan)
for d in sorted([p for p in pathlib.Path(REPO).rglob("*") if p.is_dir()]):
    if d.name == ".git": 
        continue
    try:
        if not any(d.iterdir()):
            empty_dirs.append(str(d.relative_to(REPO)))
    except Exception:
        pass

report = {
    "ts": int(time.time()),
    "zero_byte_files": zero_files,
    "empty_dirs": empty_dirs,
    "junk_files": junk_files,
    "broken_symlinks": broken_links,
    "non_utf8_files": non_utf8_files,
    "large_non_lfs": large_non_lfs,
    "secrets_hits": secrets_hits,
    "apply_mode": APPLY
}

OUT_FILE = OUT/"clean_report.json"
OUT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(f"Wrote report → {OUT_FILE}")

if APPLY:
    # Remove files first
    for rel in junk_files + zero_files:
        p = pathlib.Path(REPO)/rel
        if p.exists() and p.is_file():
            try: p.unlink()
            except: pass

    # Remove empty dirs deepest-first
    for rel in sorted(empty_dirs, key=lambda s: s.count("/"), reverse=True):
        d = pathlib.Path(REPO)/rel
        try:
            if d.exists() and d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        except: pass

    print("Cleanup applied.")
