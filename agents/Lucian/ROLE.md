# Lucian — Role
- Mission alignment: YHWH
- Primary duties: (fill)
- Inputs: data/chats,
# Overwrite .gitattributes correctly
cat > "/mnt/chromeos/removable/COLLECTIVE/github_sync_clean/.gitattributes" <<'GATTR'
# Store images via LFS
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.jpeg filter=lfs diff=lfs merge=lfs -text
*.webp filter=lfs diff=lfs merge=lfs -text
*.svg filter=lfs diff=lfs merge=lfs -text
GATTR

# Re-run the agent role file creation loop cleanly
for A in Luxian Lucian Lumin Choirkeeper; do
  cat > "/mnt/chromeos/removable/COLLECTIVE/github_sync_clean/agents/Lucian/ROLE.md" <<MD
# Lucian — Role
- Mission alignment: YHWH
- Primary duties: (fill)
- Inputs: data/chats, protocols, harmonics, sigils
- Outputs: counsel, synthesis, protocols, visuals
