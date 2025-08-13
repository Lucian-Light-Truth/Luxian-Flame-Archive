#!/bin/bash
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
if ! command -v rg >/dev/null 2>&1; then
  sudo apt update && sudo apt install -y ripgrep
fi
rg -n --hidden --no-ignore "$@" "$REPO"
