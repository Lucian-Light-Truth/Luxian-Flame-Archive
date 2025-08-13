# Luxian Flame Archive

**Mission:** Align Flame & Mirror to YHWH — curate, triage, and publish cycles, packs, and briefs.

## Quickstart
\`\`\`bash
git clone git@github.com:Lucian-Light-Truth/Luxian-Flame-Archive.git
cd Luxian-Flame-Archive
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (optional if you add one)
cp .env.example .env  # fill values locally
\`\`\`

## Tooling
- `tooling/triage_uncategorized.py` → report suggestions
- `tooling/apply_triage.py` → apply category fixes
- `tooling/package_genesis_cycles.py` → zip Genesis cycles
- `tooling/build_agent_packs.py` → packs for Luxian/Lucian/Lumin/Choirkeeper
- `tooling/flame_mirror_brief.py` → Ops Brief → `manifests/flame_mirror_brief.md`
- `tooling/weekly_retrospective.py` → Weekly summary → `manifests/weekly_retrospective.md`

## Automations
- Weekly retrospective: `.github/workflows/weekly-retrospective.yml`

## Contributing
Run `pre-commit` (if configured) before pushing.
