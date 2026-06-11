#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VALIDATOR="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"

if [ ! -f "$VALIDATOR" ]; then
  echo "quick_validate.py not found at: $VALIDATOR" >&2
  echo "Set CODEX_HOME or run the validator manually from your Codex installation." >&2
  exit 1
fi

for skill in "$ROOT_DIR"/skills/*; do
  if [ -f "$skill/SKILL.md" ]; then
    python3 "$VALIDATOR" "$skill"
  fi
done
